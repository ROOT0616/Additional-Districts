"""Queue lifecycle and definition regressions. This does not simulate native refunds or AI outcomes."""
import sys,json,argparse
from copy import deepcopy
from collections import Counter
sys.dont_write_bytecode=True
from test_balance import *

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report');args=ap.parse_args();cases=Counter()
 specs=[('sky_cities','large_scale_air_area_construction',2),('under_water_cities','large_scale_water_area_construction',5),('underground_cities','large_scale_underground_area_construction',5),('solar_power_generation','solar_power_generation',5)]
 transfer=next(b for typ,_,b in load('events/AD_artificial_queue_events.txt') if typ=='planet_event')
 for suffix,name,cap in specs:
  d=D['decision_ad_'+name]
  for natural in range(cap):
   for artificial in range(cap-natural):
    original=state();original['deposits'].update({'d_ad_'+suffix:natural,'d_ad_artificial_'+suffix:artificial});original.update(owner_id=1,planet_id=55)
    apply(first(d,'on_queued'),original)
    assert check(T['ad_valid_artificial_project_'+suffix],original)
    assert not check(first(d,'abort_trigger'),original)
    for reason in ('manual','tech','surface','ownerless','capacity','transfer','legacy','normal'):
     s=deepcopy(original);before=s['deposits'].copy();bank=s['bank'].copy()
     if reason=='manual':apply(first(d,'on_unqueued'),s)
     elif reason=='tech':s['tech']=set()
     elif reason=='surface':s['set']='habitat'
     elif reason=='ownerless':s['colony']=False;s['owner_exists']=False
     elif reason=='capacity':s['deposits']['d_ad_'+suffix]+=cap
     elif reason=='transfer':
      s.update(owner_id=2,old_owner_id=1,old_owner_exists=True)
      apply(first(transfer,'immediate'),s)
      assert 'ad_artificial_sponsor@55' not in s['country_flags'][1]
      assert s['flag_days']['ad_artificial_transfer_pause']==3
      assert not check(T['ad_can_start_artificial_'+suffix],s)
     elif reason=='legacy':s['flags'].discard('ad_artificial_tracked');s['country_flags']={}
     success=reason in ('normal','legacy')
     if not success and reason!='manual':assert check(first(d,'abort_trigger'),s)
     current=s['deposits'].copy();apply(first(d,'effect'),s)
     assert s['deposits']['d_ad_artificial_'+suffix]==current['d_ad_artificial_'+suffix]+success
     assert s['deposits']['d_ad_'+suffix]==current['d_ad_'+suffix]
     assert s['bank']==bank # script performs no extra charge/refund, native payment is outside this model
     assert not any(f.startswith('ad_artificial_project') for f in s['flags'])
     apply(first(d,'effect'),s);assert s['deposits']['d_ad_artificial_'+suffix]==current['d_ad_artificial_'+suffix]+success
     if reason=='transfer':
      s['flags'].discard('ad_artificial_transfer_pause');assert check(T['ad_can_start_artificial_'+suffix],s)
      apply(first(d,'on_queued'),s);assert check(T['ad_valid_artificial_project_'+suffix],s)
     cases['queue_'+reason]+=1
    # Aborting and cancelling both release state, without touching natural/artificial deposits.
    s=deepcopy(original);apply(first(d,'abort_effect'),s);assert s['deposits']==before and not s['flags'];cases['abort_cleanup']+=1
  # Dynamic owner flags must distinguish two planets owned by the same country.
  a=state();b=state();shared={};a.update(planet_id=10,country_flags=shared);b.update(planet_id=20,country_flags=shared)
  apply(first(d,'on_queued'),a);apply(first(d,'on_queued'),b);apply(first(d,'on_unqueued'),a)
  assert check(T['ad_valid_artificial_project_'+suffix],b);cases['independent_planets']+=1
 jobs={n:b for n,_,b in load('common/pop_jobs/AD_pop_jobs.txt') if isinstance(b,list)}
 # A gestalt city/ring must not receive any normal jobs from development districts.
 development={'government_district','university_district','residential_area','shipbuilding_arsenal','communication_area','tourist_area','defense_zone','conceptual_zone','special_research_zone','spaceport_area','orbital_elevator'}
 normal_prefixes=('job_politician_','job_bureaucrat_','job_clerk_','job_entertainer_','job_soldier_','job_trader_','job_physicist_','job_biologist_','job_engineer_')
 for name,_,body in load('common/districts/AD_districts.txt'):
  if name not in {'district_ad_'+x for x in development}:continue
  for kind,cl in [('standard','pc_ocean'),('city_world','pc_city'),('ring_world','pc_ringworld_habitable')]:
   s=state();s.update(gestalt=True,set=kind);s['class']=cl;total=0
   for k,_,v in body:
    if k=='triggered_planet_modifier' and check(first(v,'potential',[]),s):
     for key,_,value in first(v,'modifier',[]):
      if key.startswith('job_'):
       assert not key.startswith(normal_prefixes),(name,kind,key)
       if key.startswith('job_ad_'):assert key.endswith('_drone_add'),(name,kind,key)
       total+=int(value)
   assert total>0,(name,kind)
   cases['gestalt_development_jobs']+=1
 assert first(first(jobs['ad_psp'],'country_modifier'),'intel_encryption_add')=='0.1'
 assert first(jobs['ad_journalist'],'country_modifier') is None
 assert first(first(jobs['ad_congressman'],'planet_modifier'),'planet_stability_add')=='2'
 for suffix in ('','_drone'):
  assert first(first(jobs['ad_entrepreneur'+suffix],'planet_modifier'),'planet_jobs_trade_produces_mult')=='0.01'
  assert first(first(jobs['ad_spaceport_mechanics'+suffix],'country_modifier'),'country_naval_cap_add')=='4'
 for n,b in jobs.items():
  cat=first(b,'category')
  if cat in ('simple_drone','complex_drone'):
   assert first(first(b,'weight'),'weight')==('@simple_drone_job_weight' if cat=='simple_drone' else '@complex_drone_job_weight')
   assert first(first(b,'possible'),'simple_drone_trigger' if cat=='simple_drone' else 'can_think')=='yes'
   assert first(first(b,'planet_modifier',[]),'planet_amenities_add') is None
   cases['drone_job']+=1
 for file in ('common/districts/AD_districts.txt','common/buildings/AD_buildings.txt'):
  for n,_,b in load(file):
   if not isinstance(b,list):continue
   assert first(b,'ai_resource_production') is None,n
   assert not any(k=='job_culture_worker_add' for k,_,v in walk(b))
   if 'districts/' in file:
    for k,_,v in b:
     if k=='triggered_planet_modifier':assert not any(pk=='is_ai' for pk,_,pv in walk(first(v,'potential',[])))
    assert not any(k=='job_synapse_drone_add' for k,_,v in walk(b))
   cases['real_ai_estimates']+=1
 # Every custom drone tooltip referenced by a district must have JP/EN text.
 for lang in ('japanese','english'):
  loc=(M/f'localisation/AD_l_{lang}.yml').read_text(encoding='utf-8-sig')
  for k,_,v in walk(load('common/districts/AD_districts.txt')):
   if k=='text' and isinstance(v,str) and v.startswith('job_ad_') and v.endswith('_drone_effect_desc'):
    assert '\n '+v+':' in loc;cases['drone_tooltip']+=1
 buildings={n:b for n,_,b in load('common/buildings/AD_buildings.txt') if isinstance(b,list)}
 for name,_,b in load('common/districts/AD_districts.txt'):
  if name not in ('district_ad_special_tourism_zone','district_ad_orbital_elevator'):continue
  for gestalt in (False,True):
   s=state();s['gestalt']=gestalt;mods=Counter()
   for k,_,v in b:
    if k=='triggered_planet_modifier' and check(first(v,'potential',[]),s):
     for mk,_,mv in first(v,'modifier',[]):mods[mk]+=float(mv)
   key='planet_amenities_no_happiness_add' if gestalt else 'planet_amenities_add'
   assert mods[key]==500
   if gestalt:assert not mods['pop_happiness'] and not mods['planet_amenities_add']
   cases['district_amenities']+=1
 assert first(first(buildings['building_ad_P_Police'],'country_modifier'),'intel_encryption_add')=='0.5'
 assert first(first(buildings['building_pirate_broad'],'country_modifier'),'intel_encryption_add')=='-1'
 for name in ('building_ad_D_Auto','building_ad_Anti_b_pit'):assert first(buildings[name],'country_modifier') is None
 result={'version':'2.1.0-beta.6','engine_test':False,'cases':sum(cases.values()),'groups':dict(cases),'limits':'Queue callback order, native costs/refunds, job units and long-term AI construction require engine verification.'}
 if args.report:Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
