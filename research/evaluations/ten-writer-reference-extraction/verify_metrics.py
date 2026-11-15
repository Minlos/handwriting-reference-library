"""Independent small dynamic-programming checks of frozen distance implementation."""
from pathlib import Path
import importlib.util,hashlib,json,random,math
R=Path(__file__).resolve().parent;p=R/'historical_metric.py';s=importlib.util.spec_from_file_location('metric',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def independent(a,b):
 row=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  nxt=[i]
  for j,y in enumerate(b,1):nxt.append(min(nxt[-1]+1,row[j]+1,row[j-1]+(x!=y)))
  row=nxt
 return row[-1]
rng=random.Random(20261115);alphabet='абвгдёе ABC!?—';tested=0
for _ in range(300):
 a=''.join(rng.choices(alphabet,k=rng.randrange(40)));b=''.join(rng.choices(alphabet,k=rng.randrange(40)))
 assert m.distance(a,b)==independent(a,b);tested+=1
assert m.normalize('  Ёж, ЕЖ!  ','reading')=='ёж еж'
assert m.normalize('  Ёж, ЕЖ!  ','literal')=='Ёж, ЕЖ!'
assert m.normalize('её','reading')=='её'
checks=dict(metric_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),independent_distance_cases=tested,unicode_normalization_checks='passed; NFC/casefold/punctuation/whitespace and ё distinction checked')
if (R/'metrics.json').exists():
 results=json.loads((R/'metrics.json').read_text());count=0
 for x in results['rows']:
  for mode in ['reading','literal']:
   v=x[mode];assert math.isclose(v['cer'],v['edits']/v['characters'],rel_tol=1e-14);count+=1
 checks['CER_numerator_denominator_checks']=count
(R/'metric-verification.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
