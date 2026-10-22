"""Evaluate the actual generation AST; this is not the Stellaris engine."""
from pathlib import Path
from collections import Counter,defaultdict
from copy import deepcopy
import random,json,argparse,sys
sys.dont_write_bytecode=True
from clausewitz import parse,first,errors
M=Path(__file__).resolve().parents[1]
def load(rel):return parse((M/rel).read_text(encoding='utf-8-sig'),rel)
T={n:b for n,_,b in load('common/scripted_triggers/AD_natural_generation_triggers.txt')}
E={n:b for n,_,b in load('common/scripted_effects/AD_natural_generation_effects.txt')}
classes=['continental','tropical','ocean','desert','arid','savannah','arctic','tundra','alpine','gaia','relic']
energy={'geothermal_electric_power_generation','tidal_current_generation'}
mining={'open_pit_ore_deposits','under_water_deposits','orbital_deposits','high_quality_deposits','low_quality_deposits'}
farming={'shed_cultivation_land','in_water_ecosystem','mycorrhizal_communities','large_scale_grazing_land','large_scale_agricultural_land'}
rare={'archaeological_cities','ancient_ruins','ancient_databank','natural_nuclear_power_generation','sky_cities','water_cities','under_water_cities','underground_cities','natural_fortress','special_tourism_zone'}
natural=energy|mining|farming|rare
def compare(a,op,b):return {'=':a==b,'!=':a!=b,'<':a<b,'<=':a<=b,'>':a>b,'>=':a>=b}[op]
class Planet:
 def __init__(self,cl,size,seed,enabled=True,ring=False,moon=False,district_set='standard'):
  self.cl='pc_'+cl;self.size=size;self.flags={'unrelated_flag'};self.global_flags={'ad_ng_v3_enabled'} if enabled else set()
  self.deposits=Counter();self.rng=random.Random(seed);self.ring=ring;self.moon=moon;self.district_set=district_set
  self.groups=[];self.additions=[];self.draws=0
 def check(self,body):
  vals=[]
  for k,o,v in body:
   if k=='is_planet_class':x=self.cl==v
   elif k=='uses_district_set':x=self.district_set==v
   elif k=='has_global_flag':x=v in self.global_flags
   elif k=='has_planet_flag':x=v in self.flags
   elif k=='has_deposit':x=self.deposits[v]>0
   elif k=='has_ring':x=self.ring==(v=='yes')
   elif k=='has_moon':x=self.moon==(v=='yes')
   elif k=='planet_size':x=compare(self.size,o,int(v))
   elif k=='OR':x=any(self.check([a]) for a in v)
   elif k=='AND':x=self.check(v)
   elif k=='NOT':x=not self.check(v)
   elif k in T:x=self.check(T[k])==(v=='yes')
   else:raise AssertionError(('unknown trigger',k))
   vals.append(x)
  return all(vals)
 def apply(self,body):
  branch=False
  for k,o,v in body:
   if k=='if':
    branch=self.check(first(v,'limit',[]))
    if branch:self.apply([x for x in v if x[0]!='limit'])
   elif k=='else_if':
    if not branch and self.check(first(v,'limit',[])):
     self.apply([x for x in v if x[0]!='limit']);branch=True
   elif k=='else':
    if not branch:self.apply(v)
    branch=True
   elif k=='random_list':
    choices=[]
    for weight,_,b in v:
     w=float(weight)
     for mk,_,mv in b:
      if mk=='modifier' and self.check([x for x in mv if x[0]!='factor']):w*=float(first(mv,'factor'))
     if w>0:choices.append((w,[x for x in b if x[0]!='modifier']))
    assert choices,'No eligible random choice'
    self.draws+=1;roll=self.rng.random()*sum(w for w,b in choices)
    for w,b in choices:
     roll-=w
     if roll<0:self.apply(b);break
    else:raise AssertionError('Invalid weighted draw')
   elif k=='set_planet_flag':self.flags.add(v)
   elif k=='remove_planet_flag':self.flags.discard(v)
   elif k=='add_deposit':
    self.deposits[v]+=1
    phase='rare' if 'ad_ng_rare' in self.flags else 'secondary' if 'ad_ng_secondary' in self.flags else 'primary'
    self.additions.append((v[5:],phase))
   elif k=='while':
    for _ in range(int(first(v,'count'))):self.apply([x for x in v if x[0]!='count'])
   elif k in E:
    if k in ('ad_ng_choose_energy','ad_ng_choose_mining','ad_ng_choose_farming'):
     self.groups.append((k[len('ad_ng_choose_'):],'secondary' if 'ad_ng_secondary' in self.flags else 'primary'))
    self.apply(E[k])
   else:raise AssertionError(('unknown effect',k))
 def generate(self):self.apply(E['ad_ng_generate_planet'])

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report');a=ap.parse_args()
 assert not errors
 assert len(natural)==22
 deps=load('common/deposits/AD_deposits.txt')
 all_custom=[n for n,_,b in deps if isinstance(b,list) and n.startswith('d_ad_')]
 for n,_,b in deps:
  if n.startswith('d_ad_') and n[5:] in natural:
   assert first(first(b,'drop_weight'),'weight')=='0'
   assert first(b,'use_for_min_max_adjustments')=='no'
 tests=0;summary=[];total_rare=0;secondaries=Counter();primary=defaultdict(Counter);seen=set()
 for ci,cl in enumerate(classes):
  for size in (14,19,25):
   slots=Counter();types=Counter()
   for i in range(1000):
    p=Planet(cl,size,ci*1000000+size*10000+i,ring=i%2==0,moon=i%3==0)
    p.deposits['d_arid_highlands']=3
    p.generate()
    added={k:v for k,v in p.deposits.items() if k[5:] in natural and v}
    assert sum(added.values())<=8 and len(added)<=3,(cl,size,added)
    assert p.deposits['d_arid_highlands']==3
    assert not(p.deposits['d_ad_high_quality_deposits'] and p.deposits['d_ad_low_quality_deposits'])
    assert p.flags=={'unrelated_flag','ad_ng_v3_checked'}
    assert len({g for g,phase in p.groups})==len(p.groups)
    for dep,count in added.items():
     assert p.check(T['ad_ng_can_'+dep[5:]]),(cl,dep)
     seen.add(dep[5:])
    for phase in ('primary','secondary','rare'):
     values=[d for d,ph in p.additions if ph==phase]
     assert len(set(values))<=1
     max_count={'primary':2 if size<15 else 3 if size<20 else 4,'secondary':0 if size<15 else 1 if size<20 else 2,'rare':1 if size<20 else 2}[phase]
     assert len(values)<=max_count
    main_group=next((g for g,ph in p.groups if ph=='primary'),'none');primary[cl][main_group]+=1
    secondary=any(ph=='secondary' for g,ph in p.groups);secondaries[size]+=secondary
    total_rare+=any(ph=='rare' for _,ph in p.additions)
    snapshot=(p.deposits.copy(),p.flags.copy(),p.draws)
    p.generate();assert snapshot==(p.deposits,p.flags,p.draws)
    slots[sum(added.values())]+=1;types[len(added)]+=1;tests+=1
   summary.append({'class':cl,'size':size,'samples':1000,'mean_feature_copies':sum(k*v for k,v in slots.items())/1000,'mean_types':sum(k*v for k,v in types.items())/1000,'max_feature_copies':max(slots)})
 assert seen==natural,('Unreachable features',natural-seen)
 for cl in ('continental','tropical','ocean','savannah','gaia'):
  for group,rate in {'none':.2,'energy':.25,'mining':.3,'farming':.25}.items():assert abs(primary[cl][group]/3000-rate)<.035,(cl,primary[cl])
 for cl in ('arid','desert','arctic','tundra','alpine','relic'):
  assert not primary[cl]['farming']
  for group,rate in {'none':20/75,'energy':25/75,'mining':30/75}.items():assert abs(primary[cl][group]/3000-rate)<.035,(cl,primary[cl])
 assert secondaries[14]==0
 assert abs(secondaries[19]/11000-.2)<.015
 assert abs(secondaries[25]/11000-.35)<.015
 assert abs(total_rare/33000-.15)<.01
 # Old saves, unsupported classes/sets, authored deposits and re-terraforming.
 for cl in classes:
  p=Planet(cl,25,7,enabled=False);before=(p.deposits.copy(),p.flags.copy());p.generate();assert before==(p.deposits,p.flags);tests+=1
 for cl in ('city','toxic','nuked','barren','gas_giant','hive','machine','ringworld_habitable'):
  p=Planet(cl,25,7);p.generate();assert p.deposits=={} and p.flags=={'unrelated_flag'};tests+=1
 for ds in ('city_world','ring_world','habitat','machine_world','hive_world'):
  p=Planet('continental',25,7,district_set=ds);p.generate();assert not p.deposits and p.draws==0;tests+=1
 for n in all_custom:
  p=Planet('continental',25,7);p.deposits[n]=12;before=p.deposits.copy();p.generate();assert p.deposits==before and p.draws==0;tests+=1
 p=Planet('barren',25,17);p.generate();assert p.draws==0
 p.cl='pc_ocean';p.generate();snapshot=(p.deposits.copy(),p.flags.copy(),p.draws)
 p.cl='pc_desert';p.generate();assert snapshot==(p.deposits,p.flags,p.draws);tests+=1
 actions={n:b for n,_,b in load('common/on_actions/AD_on_actions.txt')}
 assert not any(v=='additionaldistricts.9000' for k,_,v in first(actions['on_single_player_save_game_load'],'events'))
 for name in ('on_terraforming_complete','on_planet_class_changed','on_planet_surveyed'):
  assert (None,None,'additionaldistricts.9003') in first(actions[name],'events')
 assert 'on_survey_planet' not in actions
 event=next(b for k,_,b in load('events/AD_spawn.txt') if k=='event')
 assert first(event,'fire_only_once')=='yes'
 delayed={first(b,'id'):b for k,_,b in load('events/AD_natural_generation.txt') if k=='planet_event'}
 scheduler=first(first(delayed['additionaldistricts.9003'],'immediate'),'planet_event')
 assert first(scheduler,'id')=='additionaldistricts.9004' and first(scheduler,'days')=='1'
 assert first(first(delayed['additionaldistricts.9004'],'immediate'),'ad_ng_generate_planet')=='yes'
 assert first(delayed['additionaldistricts.9003'],'trigger')==first(delayed['additionaldistricts.9004'],'trigger')
 result={'version':'2.1.0-beta.3','engine_test':False,'cases':tests,'reachable_natural_types':len(seen),'rare_rate':total_rare/33000,'secondary_rates':{str(k):v/11000 for k,v in secondaries.items()},'primary_distribution':{k:{g:v/3000 for g,v in d.items()} for k,d in primary.items()},'summary':summary}
 if a.report:Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k not in ('summary','primary_distribution')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
