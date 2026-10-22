"""Evaluate beta.5 definitions, not the Stellaris engine."""
import json,sys
from collections import Counter
sys.dont_write_bytecode=True
from test_balance import load,first,walk,check,state,apply,E
from test_natural_generation import Planet

jobs={n:b for n,_,b in load('common/pop_jobs/AD_pop_jobs.txt') if isinstance(b,list)}
cases=0
for suffix in ('','_drone'):
 j=jobs['ad_data_minor'+suffix]
 assert first(first(j,'country_modifier'),'intel_encryption_add')=='0.1'
 assert first(first(j,'planet_modifier'),'planet_researchers_produces_mult')=='0.01'
 assert dict((k,float(v)) for k,_,v in first(first(j,'resources'),'produces'))=={r:2 for r in ('physics_research','society_research','engineering_research')}
 assert dict((k,float(v)) for k,_,v in first(first(j,'resources'),'upkeep'))=={'energy' if suffix else 'consumer_goods':3}
 rate=float(first(first(jobs['ad_shipwright'+suffix],'country_modifier'),'starbase_shipyard_build_speed_mult'))
 for count in (0,.5,1,5,20,80,100,200,1000,10000):
  assert abs(rate*count-.0025*count)<1e-10
  if count>=100:assert rate*count>.2
  cases+=1
deps=load('common/deposits/AD_deposits.txt');districts={n:b for n,_,b in load('common/districts/AD_districts.txt')}
reviewed=0
for name,_,body in deps:
 if not isinstance(body,list):continue
 if not any(k=='has_planet_flag' and v=='ad_ng_v5_native_resources' for k,_,v in walk(body)):continue
 reviewed+=1
 for gestalt in (False,True):
  for new in (False,True):
   for copies in (1,2,4):
    s=state();s['gestalt']=gestalt
    if new:s['flags'].add('ad_ng_v5_native_resources')
    mods=Counter()
    for k,_,v in body:
     if k=='triggered_planet_modifier' and check(first(v,'potential'),s):
      mods.update({mk:float(mv)*copies for mk,_,mv in v if mk!='potential'})
    custom='district_ad_'+name[5:]+'_max_add'
    if not gestalt or new:
     assert mods=={custom:copies},(name,gestalt,new,mods)
    else:
     assert custom not in mods
     assert any(k in mods for k in ('district_generator_max_add','district_mining_max_add','district_farming_max_add'))
    cases+=1
 # The machine-only branch must not duplicate the common gestalt workforce.
 d=districts['district_ad_'+name[5:]]
 for k,_,v in d:
  if k=='triggered_planet_modifier' and any(pk=='is_machine_empire' for pk,_,pv in walk(first(v,'potential',[]))):
   assert not any(mk.startswith('job_') for mk,_,mv in first(v,'modifier',[]))
assert reviewed==13
for enabled in (False,True):
 for preexisting in (False,True):
  p=Planet('ocean',25,123,enabled=enabled)
  if preexisting:p.deposits['d_ad_tidal_current_generation']=2
  p.generate()
  assert ('ad_ng_v5_native_resources' in p.flags)==(enabled and not preexisting)
  before=(p.deposits.copy(),p.flags.copy());p.generate()
  assert before==(p.deposits,p.flags)
  cases+=1
print(json.dumps({'version':'2.1.0-beta.5','cases':cases,'engine_test':False,'gestalt_features':reviewed}))
