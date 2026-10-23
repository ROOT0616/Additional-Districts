"""Exercise save cleanup and deposit-based development after removing cached flags."""
import sys,json,argparse
from copy import deepcopy
from collections import Counter
sys.dont_write_bytecode=True
from test_balance import *

def fire(event,world):
 if not check(first(event,'trigger',[]),world):return False
 for key,op,value in first(event,'immediate'):
  if key in ('every_country','every_galaxy_planet'):
   for s in world['countries' if key=='every_country' else 'planets']:
    s['global_flags']=world.setdefault('global_flags',set());apply(value,s)
  else:apply([(key,op,value)],world)
 return True

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report');args=ap.parse_args();tests=Counter()
 cleanup=next(b for k,_,b in load('events/AD_shipwright_events.txt') if k=='event')
 native=load('common/on_actions/AD_on_actions.txt')
 assert not any(k=='on_monthly_pulse_country' for k,_,v in native)
 assert not any(v in ('additionaldistricts.9002','additionaldistricts.9010') for k,_,v in walk(native) if isinstance(v,str))
 cm=first(first(cleanup,'immediate'),'every_country');pm=first(first(cleanup,'immediate'),'every_galaxy_planet')
 country_flags={v for k,_,v in cm if k=='remove_country_flag'};planet_flags={v for k,_,v in pm if k=='remove_planet_flag'}
 assert len(country_flags)==26 and len(planet_flags)==41
 for countries in (0,1,10):
  for planets in (0,1,10):
   world=state();world['countries']=[state() for _ in range(countries)];world['planets']=[state() for _ in range(planets)]
   for c in world['countries']:
    c['country_flags']={1:country_flags|{'keep_country_flag'}};c['modifiers']={'ad_shipwright_support_'+str(n):True for n in (1,3,5,10,15,20)};c['modifiers']['keep_modifier']=True
   for p in world['planets']:
    p['flags']=planet_flags|{'ad_ng_v3_checked','ad_ng_v5_native_resources','ad_artificial_project','do_ad_under_water_cities'};p['deposits'].update({'d_ad_under_water_cities':2,'d_ad_artificial_under_water_cities':3});p['jobs']={'ad_shipwright':500}
   before=[(p['deposits'].copy(),p['jobs'].copy()) for p in world['planets']]
   assert fire(cleanup,world)
   for c in world['countries']:assert c['country_flags'][1]=={'keep_country_flag'} and c['modifiers']=={'keep_modifier':True}
   for p,(deps,jobs) in zip(world['planets'],before):
    assert p['flags']=={'ad_ng_v3_checked','ad_ng_v5_native_resources','ad_artificial_project','do_ad_under_water_cities'} and p['deposits']==deps and p['jobs']==jobs
   saved=deepcopy(world);assert not fire(cleanup,world) and world==saved;tests['one_time_cleanup']+=1
 # Compare every combination of 11 specializations; caches are no longer consulted or written.
 suffixes=[n[len('ad_add_development_'):] for n in E if n.startswith('ad_add_development_')];assert len(suffixes)==11
 for mask in range(1<<11):
  for suffix in suffixes:
   s=state();s['flags']={'keep_flag','do_ad_1','do_ad_4'};s['deposits'].update({'d_ad_'+x:1 for i,x in enumerate(suffixes) if mask>>i&1})
   before=s['deposits'].copy();count=sum(before.values());present=before['d_ad_'+suffix]>0
   apply(E['ad_add_development_'+suffix],s)
   assert s['deposits']['d_ad_'+suffix]==int(present or count<4)
   assert s['flags']=={'keep_flag','do_ad_1','do_ad_4'};tests['development_add']+=1
   s=state();s['deposits']=before.copy();apply(E['ad_remove_development_'+suffix],s)
   assert s['deposits']['d_ad_'+suffix]==0
   assert sum(s['deposits'].values())==count-present;tests['development_remove']+=1
 for suffix in suffixes:
  for busy,built in ((True,0),(False,1)):
   s=state();s['deposits']['d_ad_'+suffix]=1;s.update(construction=busy,built=built);apply(E['ad_remove_development_'+suffix],s)
   assert s['deposits']['d_ad_'+suffix]==1;tests['removal_guard']+=1
 migration=next(b for k,_,b in load('events/AD_artificial_migration.txt') if k=='event')
 for ambiguous in (False,True):
  world=state();p=state();p['deposits']['d_ad_under_water_cities']=5;p['flags'].add('do_ad_water_cities_5' if ambiguous else 'do_ad_under_water_cities');world.update(planets=[p],countries=[])
  assert fire(migration,world)
  assert p['deposits']['d_ad_under_water_cities']==(5 if ambiguous else 0)
  assert p['deposits']['d_ad_artificial_under_water_cities']==(0 if ambiguous else 5)
  saved=deepcopy(world);assert not fire(migration,world) and world==saved;tests['legacy_migration']+=1
 assert len(S)==6 and all(first(b,'starbase_shipyard_build_speed_mult')=='0' for b in S.values())
 tests['neutral_modifier_ids']+=6
 result={'version':'2.1.0-beta.7','engine_test':False,'cases':sum(tests.values()),'groups':dict(tests),'limits':'Actual old-save load order and timing improvements require engine verification.'}
 if args.report:Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
