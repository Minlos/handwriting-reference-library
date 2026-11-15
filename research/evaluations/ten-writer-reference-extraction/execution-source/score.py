"""Frozen whole-document metrics; repetitions averaged within writer; paired writer bootstrap."""
from pathlib import Path
import json,hashlib,importlib.util,random,statistics,collections
R=Path(__file__).resolve().parent;W=R.parents[1];mp=R/'historical_metric.py'
spec=importlib.util.spec_from_file_location('frozen_metric',mp);metric=importlib.util.module_from_spec(spec);spec.loader.exec_module(metric)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
writers=json.loads((R/'protocol.json').read_text())['writers'];rows=[];fail=[]
for w in writers:
 gold=(R/'evaluator'/'published'/f'writer{w:03}.txt').read_text();pages=json.loads((R/'groups'/f'writer{w:03}'/'targets.json').read_text())['pages']
 docs=[];bp=[R/'russian-crnn'/(p['id']+'.json') for p in pages]
 if all(p.exists() for p in bp):
  rs=[json.loads(p.read_text()) for p in bp]
  if all(x['status']=='completed' for x in rs):docs.append(('russian-crnn','A',1,'\n'.join(x['prediction'] for x in rs),[H(p) for p in bp]))
  else:fail.append(dict(model='russian-crnn',writer=w,reason='page failure'))
 for model in ['astra','sol','deepseek']:
  for c in 'ABC':
   for rep in [1,2]:
    p=R/'predictions'/model/c/f'rep{rep}'/f'writer{w:03}.json'
    if not p.exists():continue
    obj=json.loads(p.read_text())
    if obj['status']!='completed':fail.append(dict(model=model,condition=c,replicate=rep,writer=w,reason=obj.get('error',obj['status'])));continue
    assert [x['id'] for x in obj['pages']]==[x['id'] for x in pages],p
    docs.append((model,c,rep,'\n'.join(x['prediction'] for x in obj['pages']),[H(p)]))
 for model,c,rep,hyp,hashes in docs:
  rows.append(dict(model=model,condition=c,replicate=rep,writer=w,target_pages=len(pages),prediction_hashes=hashes,unknown_markers=hyp.count('[неразборчиво]'),**{m:metric.score(gold,hyp,m) for m in ['reading','literal']}))
for p in (R/'deepseek-api').glob('writer*-rep*.json'):
 if p.name.endswith(('-inputs.json','-raw-received.json')):continue
 obj=json.loads(p.read_text())
 if obj.get('status')=='error':fail.append(dict(model='deepseek',writer=obj['writer'],condition=obj['condition'],replicate=obj['replicate'],reason=obj.get('error','error')))
# Each writer/condition row averages repeated CER and edit counts; never treats repetitions as writers.
lookup={}
for x in rows:lookup.setdefault((x['model'],x['condition'],x['writer']),[]).append(x)
means={k:{m:{f:statistics.mean(x[m][f] for x in v) for f in ['cer','edits','characters']} for m in ['reading','literal']} for k,v in lookup.items()}
aggregates=[]
for model,c in sorted({(x['model'],x['condition']) for x in rows}):
 ws=[w for w in writers if (model,c,w) in means]
 aggregates.append(dict(model=model,condition=c,writers=len(ws),repetitions_per_writer={str(w):len(lookup[model,c,w]) for w in ws},**{m:dict(mean_writer_CER=statistics.mean(means[model,c,w][m]['cer'] for w in ws),pooled_CER=sum(means[model,c,w][m]['edits'] for w in ws)/sum(means[model,c,w][m]['characters'] for w in ws)) for m in ['reading','literal']}))
def compare(model,c,b,m,ws):
 diff={w:means[model,c,w][m]['cer']-means[model,b,w][m]['cer'] for w in ws};rng=random.Random(20261115);ds=[];rs=[]
 for _ in range(10000):
  sample=rng.choices(ws,k=len(ws));aa=sum(means[model,c,w][m]['cer'] for w in sample);bb=sum(means[model,b,w][m]['cer'] for w in sample);ds.append((aa-bb)/len(ws));rs.append(100*(aa/bb-1) if bb else 0)
 ds.sort();rs.sort();base=sum(means[model,b,w][m]['cer'] for w in ws);alt=sum(means[model,c,w][m]['cer'] for w in ws)
 return dict(baseline_mean_writer_CER=base/len(ws),condition_mean_writer_CER=alt/len(ws),model=model,condition=c,baseline=b,metric=m,paired_writers=ws,denominator=len(ws),wins=sum(v<0 for v in diff.values()),ties=sum(v==0 for v in diff.values()),losses=sum(v>0 for v in diff.values()),mean_writer_CER_delta=sum(diff.values())/len(ws),paired_writer_bootstrap_95=[ds[250],ds[9750]],relative_mean_writer_CER_change_percent=100*(alt/base-1) if base else None,relative_mean_writer_CER_change_bootstrap_95=[rs[250],rs[9750]],bootstrap_seed=20261115,bootstrap_repetitions=10000)
pairs=[];complete_pairs=[]
for model in ['astra','sol','deepseek']:
 for c,b in [('B','A'),('C','A'),('C','B')]:
  ws=[w for w in writers if (model,c,w) in means and (model,b,w) in means]
  complete=[w for w in ws if len(lookup[model,c,w])==2 and len(lookup[model,b,w])==2]
  for m in ['reading','literal']:
   if ws:pairs.append(compare(model,c,b,m,ws))
   if complete:complete_pairs.append(compare(model,c,b,m,complete))
coverage=[]
for model in ['astra','sol','deepseek']:
 for c in 'ABC':
  rr=[x for x in rows if x['model']==model and x['condition']==c];ff=[x for x in fail if x['model']==model and x.get('condition')==c]
  coverage.append(dict(model=model,condition=c,expected_documents=20,valid_documents=len(rr),failed_documents=len(ff),not_finished_documents=20-len(rr)-len(ff),valid_target_page_transcriptions=sum(x['target_pages'] for x in rr),expected_target_page_transcriptions=90,writers_with_two_valid_repetitions=[w for w in writers if len(lookup.get((model,c,w),[]))==2]))
result=dict(label_status='Published, assistant correspondence-audited but not human-verified; unchanged primary labels.',metric_source_sha256=H(mp),scope='Whole held-out original document, numeric page order; repeats averaged within writer',normalization=dict(reading='NFC/casefold/remove Unicode punctuation/collapse whitespace; ё retained',literal='NFC/collapse whitespace; punctuation and case retained'),coverage=coverage,rows=rows,aggregates=aggregates,paired_writer_comparisons=pairs,complete_two_repetition_comparisons=complete_pairs,failures=fail,uncertainty_limitation='Deterministic ten-writer convenience selection; writer bootstrap measures sensitivity to this set, not population representativeness. Incomplete repeat counts are explicit.')
(R/'metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(aggregates,indent=2))
