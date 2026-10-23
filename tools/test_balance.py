"""Evaluate real definitions with a small logic model, not the game engine."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import json,argparse,sys
sys.dont_write_bytecode=True
from clausewitz import parse,first,walk,errors
M=Path(__file__).resolve().parents[1]
def load(path):return parse((M/path).read_text(encoding='utf-8-sig'),path)
T={n:b for p in (M/'common/scripted_triggers').glob('*.txt') for n,_,b in parse(p.read_text(encoding='utf-8-sig'),str(p))}
E={n:b for p in (M/'common/scripted_effects').glob('*.txt') for n,_,b in parse(p.read_text(encoding='utf-8-sig'),str(p))}
D={n:b for n,_,b in load('common/decisions/AD_decisions.txt') if isinstance(b,list)}
S={n:b for n,_,b in load('common/static_modifiers/AD_shipwright_modifiers.txt')}
def cmp(a,o,b):return {'=':a==b,'!=':a!=b,'>':a>b,'>=':a>=b,'<':a<b,'<=':a<=b}[o]
def state():return {'deposits':Counter(),'flags':set(),'built':0,'extra':0,'construction':False,'class':'pc_ocean','set':'standard','colony':True,'modifiers':{},'vars':{},'jobs':{},'bank':Counter(minerals=100000,alloys=100000,exotic_gases=100000),'income':Counter(energy=10,minerals=10),'tech':{'mixed_use_development_plan','large_scale_air_construction_technology','large_scale_in_water_construction_technology','large_scale_ground_construction_technology'},'war':False,'housing':0,'free_jobs':0,'free_district_slots':10,'designation':'col_research','capital':False,'gestalt':False,'fleet_tagged':False,'building':True,'owner_exists':True}

def country_flag(key,s):return key.replace('@root','@'+str(s.get('planet_id',1)))
def check(body,s):
 for k,o,v in body:
  if k=='OR':r=any(check([x],s) for x in v)
  elif k=='AND' or k=='owner' or k=='this' or k=='solar_system':r=check(v,s)
  elif k=='NOT':r=not check(v,s)
  elif k=='NOR':r=not any(check([x],s) for x in v)
  elif k=='has_planet_flag':r=v in s['flags']
  elif k=='has_global_flag':r=v in s.setdefault('global_flags',set())
  elif k=='calc_true_if':
   _,op,num=next(x for x in v if x[0]=='amount');r=cmp(sum(check([x],s) for x in v if x[0]!='amount'),op,int(num))
  elif k=='has_country_flag':r=country_flag(v,s) in s.setdefault('country_flags',{}).setdefault(s.get('owner_id',1),set())
  elif k=='has_deposit':r=s['deposits'][v]>0
  elif k=='has_building_construction':r=s['construction']==(v=='yes')
  elif k=='is_colony':r=s['colony']==(v=='yes')
  elif k=='uses_district_set':r=s['set']==v
  elif k=='is_planet_class':r=s['class']==v
  elif k=='has_technology':r=v in s['tech']
  elif k=='has_modifier':r=v in s['modifiers']
  elif k=='is_at_war':r=s['war']==(v=='yes')
  elif k=='is_gestalt':r=s['gestalt']==(v=='yes')
  elif k=='is_regular_empire':r=(not s['gestalt'])==(v=='yes')
  elif k=='has_designation':r=s['designation']==v
  elif k=='is_capital':r=s['capital']==(v=='yes')
  elif k=='count_deposits':
   _,op,num=next(x for x in v if x[0]=='count');r=cmp(s['deposits'][first(v,'type')],op,int(num))
  elif k=='num_free_districts':
   suffix=first(v,'type')[len('district_ad_'):];num=s['deposits']['d_ad_'+suffix]+s['deposits']['d_ad_artificial_'+suffix]+s['extra']-s['built']
   _,op,n=next(x for x in v if x[0]=='value');r=cmp(max(0,num),op,int(n))
  elif k=='num_districts':
   _,op,n=next(x for x in v if x[0]=='value');r=cmp(s.get('built_types',{}).get(first(v,'type'),s['built']),op,int(n))
  elif k=='has_monthly_income':
   _,op,n=next(x for x in v if x[0]=='value');r=cmp(s['income'][first(v,'resource')],op,float(n))
  elif k in ('has_country_resource','resource_stockpile_compare'):
   key='amount' if k=='has_country_resource' else 'value';_,op,n=next(x for x in v if x[0]==key)
   r=cmp(s['bank'][first(v,'type' if k=='has_country_resource' else 'resource')],op,float(n))
  elif k in ('free_housing','free_jobs','free_district_slots'):r=cmp(s[{'free_housing':'housing'}.get(k,k)],o,float(v))
  elif k=='check_variable':
   _,op,n=next(x for x in v if x[0]=='value');r=cmp(s['vars'][first(v,'which')],op,float(n))
  elif k=='exists':r=s['owner_exists'] if v=='owner' else s.get('old_owner_exists',False) if v=='fromfrom' else False
  elif k=='has_building':assert v=='building_ad_Anti_s_misile';r=s['building']
  elif k=='any_fleet_in_system':r=s['fleet_tagged'] and check(v,s)
  elif k=='has_fleet_flag':assert v=='ad_planet_defence@root';r=s['fleet_tagged']
  elif k in T:r=check(T[k],s)==(v=='yes')
  else:raise AssertionError(('trigger',k))
  if not r:return False
 return True
def apply(body,s):
 branch=False
 for k,o,v in body:
  if k=='if':
   branch=check(first(v,'limit',[]),s)
   if branch:apply([x for x in v if x[0]!='limit'],s)
  elif k=='else_if':
   if not branch and check(first(v,'limit',[]),s):apply([x for x in v if x[0]!='limit'],s);branch=True
  elif k=='else':
   if not branch:apply(v,s)
   branch=True
  elif k=='export_trigger_value_to_variable':
   assert first(v,'trigger')=='num_assigned_jobs';s['vars'][first(v,'variable')]=s['jobs'].get(first(first(v,'parameters'),'job'),0)
  elif k=='change_variable':s['vars'][first(v,'which')]+=s['vars'][first(v,'value')]
  elif k=='clear_variable':s['vars'].pop(v,None)
  elif k=='remove_modifier':s['modifiers'].pop(v,None)
  elif k=='add_modifier':s['modifiers'][first(v,'modifier')]=True
  elif k=='add_deposit':s['deposits'][v]+=1
  elif k=='remove_deposit':s['deposits'][v]-=1;assert s['deposits'][v]>=0
  elif k=='set_planet_flag':s['flags'].add(v)
  elif k=='set_global_flag':s.setdefault('global_flags',set()).add(v)
  elif k=='while':
   count=first(v,'count');assert count is not None
   for _ in range(int(count)):apply([x for x in v if x[0]!='count'],s)
  elif k=='remove_planet_flag':s['flags'].discard(v)
  elif k=='set_timed_planet_flag':
   s['flags'].add(first(v,'flag'));s.setdefault('flag_days',{})[first(v,'flag')]=int(first(v,'days'))
  elif k=='set_country_flag':s.setdefault('country_flags',{}).setdefault(s.get('owner_id',1),set()).add(country_flag(v,s))
  elif k=='remove_country_flag':s.setdefault('country_flags',{}).setdefault(s.get('owner_id',1),set()).discard(country_flag(v,s))
  elif k=='owner':apply(v,s)
  elif k=='fromfrom':
   current=s.get('owner_id',1);s['owner_id']=s.get('old_owner_id',0);apply(v,s);s['owner_id']=current
  elif k=='hidden_effect':apply(v,s)
  elif k=='custom_tooltip':pass
  elif k in E:apply(E[k],s)
  else:raise AssertionError(('effect',k))
def weight(b,s):
 w=float(first(b,'weight','1'))
 for k,_,v in b:
  if k=='modifier' and check([x for x in v if x[0] not in ('factor','add')],s):w=w*float(first(v,'factor','1'))+float(first(v,'add','0'))
 return w
def expected_tier(raw):
 for threshold,rate in [(8000,20),(4000,15),(2000,10),(1000,5),(500,3),(100,1)]:
  if raw>=threshold:return rate
 return 0
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report');args=ap.parse_args();tests=Counter();assert not errors
 for raw in (0,1,99,100,101,499,500,501,999,1000,1999,2000,3999,4000,7999,8000,8001,1000000):
  for drone in (0,raw//2,raw):
   s=state();s['jobs']={'ad_shipwright':raw-drone,'ad_shipwright_drone':drone,'vacant_shipwright':999999};s['modifiers']={'ad_shipwright_support_1':True,'ad_shipwright_support_20':True,'unrelated_modifier':True}
   for _ in range(3):
    apply(E['ad_refresh_shipwright_support'],s)
    found=[k for k in s['modifiers'] if k.startswith('ad_shipwright_support_')]
    assert found==[]
    assert 'unrelated_modifier' in s['modifiers'] and not s['vars']
    tests['shipwright_tiers']+=1
   s['jobs']={};apply(E['ad_refresh_shipwright_support'],s);assert list(s['modifiers'])==['unrelated_modifier'];tests['shipwright_loss']+=1
 specs=[('sky_cities','large_scale_air_area_construction',2,{'minerals':500,'alloys':250,'exotic_gases':50},180,125),('under_water_cities','large_scale_water_area_construction',5,{'minerals':200,'alloys':100},180,50),('underground_cities','large_scale_underground_area_construction',5,{'minerals':100,'alloys':200},180,50),('solar_power_generation','solar_power_generation',5,{'minerals':100},90,25)]
 for suffix,name,target,cost,days,removal in specs:
  d=D['decision_ad_'+name];undo=D['decision_ad_undo_'+name]
  assert dict((k,int(v)) for k,_,v in first(first(d,'resources'),'cost'))==cost
  assert first(d,'enactment_time')==str(days) and first(undo,'enactment_time')=='0'
  assert first(first(first(undo,'resources'),'cost'),'minerals')==str(removal)
  for natural in range(8):
   for artificial in range(7):
    for busy in (False,True):
     s=state();s['deposits']=Counter({'d_ad_'+suffix:natural,'d_ad_artificial_'+suffix:artificial});s['flags']={'ad_artificial_project'} if busy else set()
     apply(E['ad_add_artificial_one_'+suffix],s)
     assert s['deposits']['d_ad_'+suffix]==natural
     assert s['deposits']['d_ad_artificial_'+suffix]==artificial+int(not busy and natural+artificial<target)
     tests['single_add']+=1
    for extra in (0,2):
     for built in range(natural+artificial+extra+2):
      for construction in (False,True):
       s=state();s.update(extra=extra,built=built,construction=construction);s['deposits']=Counter({'d_ad_'+suffix:natural,'d_ad_artificial_'+suffix:artificial})
       expected=artificial>0 and not construction and built<natural+artificial+extra
       apply(E['ad_remove_artificial_one_'+suffix],s)
       assert s['deposits']['d_ad_artificial_'+suffix]==artificial-int(expected)
       assert s['deposits']['d_ad_'+suffix]==natural
       tests['single_remove']+=1
  # Native queue model: no early deposit, no duplicate project, cancel unlocks, completion adds once.
  s=state();assert check(first(d,'potential'),s) and check(first(d,'allow'),s)
  for r,c in cost.items():s['bank'][r]-=c
  bank=s['bank'].copy();apply(first(d,'on_queued'),s)
  assert not s['deposits'] and check(first(d,'allow'),s)
  for other in specs:assert not check(first(D['decision_ad_'+other[1]],'potential'),s)
  saved=deepcopy(s);cancelled=deepcopy(s);apply(first(d,'on_unqueued'),cancelled);assert not cancelled['flags'] and not cancelled['deposits']
  apply(first(d,'effect'),saved);assert saved['deposits']['d_ad_artificial_'+suffix]==1 and not saved['flags'] and saved['bank']==bank,(suffix,saved)
  tests['queue_model']+=7
  # AI must reject empty reserves, deficits, no build space, open projects and weak wartime reserves.
  s=state();assert weight(first(d,'ai_weight'),s)<=40
  for change in ('bank','deficit','space','jobs','unused','war'):
   x=state()
   if change=='bank':x['bank']=Counter()
   if change=='deficit':x['income']['minerals']=-1
   if change=='space':x['free_district_slots']=0
   if change=='jobs':x.update(free_jobs=1000,housing=600)
   if change=='unused':x['deposits']['d_ad_artificial_'+suffix]=1
   if change=='war':x['war']=True;x['bank']['alloys']=100
   assert weight(first(d,'ai_weight'),x)==0,(suffix,change)
   tests['ai_gates']+=1
 events=[b for k,_,b in load('events/AD_events.txt') if isinstance(b,list)]
 menu=next(b for b in events if first(b,'id')=='additionaldistricts.2')
 options=[b for k,_,b in menu if k=='option' and first(b,'name')!='CLOSE'];assert len(options)==8
 for idx,opt in enumerate(options):
  action='decision_ad_'+('undo_' if idx%2 else '')+specs[idx//2][1]
  assert first(first(first(opt,'hidden_effect'),'select_decision'),'name')==action
  assert not any(k in ('add_resource','add_deposit','remove_deposit') for k,_,v in walk(opt))
  tests['menu_delegation']+=1
 jobs={n:b for n,_,b in load('common/pop_jobs/AD_pop_jobs.txt') if isinstance(b,list)}
 for suffix in ('','_drone'):
  j=jobs['ad_professorship'+suffix];assert first(first(j,'planet_modifier'),'planet_jobs_specialist_produces_mult') is None
  assert {k:v for k,_,v in first(first(j,'resources'),'produces')}=={r:'2' for r in ('physics_research','society_research','engineering_research')}
  j=jobs['ad_shipwright'+suffix];assert first(first(j,'country_modifier'),'starbase_shipyard_build_speed_mult')=='0.0025'
  assert first(first(j,'country_modifier'),'country_naval_cap_add')=='1'
  tests['job_roles']+=2
 university=next(b for n,_,b in load('common/districts/AD_districts.txt') if n=='district_ad_university_district')
 for gestalt in (False,True):
  for kind in ('standard','city_world','ring_world'):
   s=state();s.update(gestalt=gestalt);s['class']='pc_city' if kind=='city_world' else 'pc_ocean';s['set']=kind
   mods=Counter()
   for k,_,v in university:
    if k=='triggered_planet_modifier' and check(first(v,'potential'),s):
     for mk,_,mv in first(v,'modifier',[]):
      if mk.startswith('job_'):mods[mk]+=int(mv)
   prof=mods['job_ad_professorship'+('_drone' if gestalt else '')+'_add']
   researchers=sum(v for k,v in mods.items() if k.startswith(('job_physicist','job_biologist','job_engineer','job_calculator_')))
   assert researchers==3*prof,(gestalt,kind,mods)
   assert not mods['job_ad_professorship'+('' if gestalt else '_drone')+'_add']
   tests['university_mix']+=1
 defense=next(b for b in events if first(b,'id')=='additionaldistricts.100')
 success=first(first(defense,'immediate'),'random_list')[0][2]
 assert first(first(success,'set_timed_planet_flag'),'days')=='90'
 assert first(first(first(success,'create_fleet'),'effect'),'set_fleet_flag')=='ad_planet_defence@root'
 for cooldown in (False,True):
  for live in (False,True):
   for owner in (False,True):
    s=state();s['owner_exists']=owner;s['fleet_tagged']=live
    if cooldown:s['flags'].add('ad_planet_defence_cooldown')
    assert check(first(defense,'trigger'),s)==(owner and not cooldown and not live)
    tests['defense_gates']+=1
 techs={n:b for n,_,b in load('common/technology/AD_technology.txt') if isinstance(b,list)}
 for n,b in techs.items():
  if n!='mixed_use_development_plan':assert (None,None,'mixed_use_development_plan') in first(b,'prerequisites')
 assert not any(k=='is_gestalt' for k,_,v in walk(first(techs['mixed_use_development_plan'],'weight_modifier')))
 actions={n:b for n,_,b in load('common/on_actions/AD_on_actions.txt')}
 assert 'on_monthly_pulse_country' not in actions
 assert (None,None,'additionaldistricts.9011') in first(actions['on_single_player_save_game_load'],'events')
 result={'version':'2.1.0-beta.7','engine_test':False,'cases':sum(tests.values()),'groups':dict(tests),'limits':'Native payment, queue completion/cancellation and job units require engine verification.'}
 if args.report:Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
