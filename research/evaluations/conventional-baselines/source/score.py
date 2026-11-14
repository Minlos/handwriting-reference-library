"""Score completed local baselines with each historical panel's frozen references."""
from pathlib import Path
import json,sys,collections,csv,io,hashlib
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT.parents[1]/'outputs/hwr200-expanded'));from score import score as score_text
# Import by path: this file is also named score.py.
import importlib.util
spec=importlib.util.spec_from_file_location('frozen_metric',ROOT.parents[1]/'outputs/hwr200-expanded/score.py');metric=importlib.util.module_from_spec(spec);spec.loader.exec_module(metric);score_text=metric.score

def prediction(row,record):
 text=record['prediction'];exclusions=[]
 if row['unit']=='diary3-P06':
  # User-requested exclusion of the final unresolved word, located from the actual frozen image.
  # Image is 2343x2765. The rectangle excludes that ink, not neighboring known words.
  box=[1560,2540,2150,2765]
  if isinstance(record['raw'],list):
   kept=[]
   for r in record['raw']:
    cx=sum(t[0]for t in r['box'])/len(r['box']);cy=sum(t[1]for t in r['box'])/len(r['box'])
    if box[0]<=cx<=box[2]and box[1]<=cy<=box[3]:exclusions.append({'text':r['text'],'box':r['box']})
    else:kept.append(r['text'])
   text='\n'.join(kept)
  else:
   words=list(csv.DictReader(io.StringIO(record['raw']),delimiter='\t',quoting=csv.QUOTE_NONE));groups=collections.OrderedDict()
   for w in words:
    if not w['text'].strip():continue
    cx=int(w['left'])+int(w['width'])/2;cy=int(w['top'])+int(w['height'])/2
    if box[0]<=cx<=box[2]and box[1]<=cy<=box[3]:exclusions.append(w);continue
    k=tuple(w[x]for x in ['page_num','block_num','par_num','line_num']);groups.setdefault(k,[]).append(w['text'])
   text='\n'.join(' '.join(ws)for ws in groups.values())
 return text,exclusions

def main():
 evaluator=json.load(open(ROOT/'evaluator.json'));results={};by_unit={}
 for engine in ['tesseract','easyocr']:
  records={f.stem:json.load(open(f))for f in (ROOT/engine/'records').glob('*.json')};settings=json.load(open(ROOT/engine/'settings.json'));panels={};by_unit[engine]={}
  for name,panel in evaluator['panels'].items():
   rows=[];failures=[]
   for unit in panel['records']:
    rr=[records.get(i)for i in unit['inputs']]
    if any(r is None or r['status']!='completed'for r in rr):failures.append(unit['unit']);continue
    parts=[];excluded=[]
    for r in rr:
     h,e=prediction(unit,r);parts.append(h);excluded+=e
    hyp='\n'.join(parts);ref=evaluator['gold'][unit['gold_id']];sc={mode:score_text(ref,hyp,mode)for mode in ['literal','reading']}
    row={'unit':unit['unit'],'input_ids':unit['inputs'],'input_sha256':[r['input_sha256']for r in rr],'prediction':hyp,'excluded_region_outputs':excluded,'seconds':sum(r['seconds']for r in rr),**sc};rows.append(row);by_unit[engine][unit['unit']]=row
   agg=None
   if not failures:
    agg={}
    for mode in ['literal','reading']:
     e=sum(r[mode]['edits']for r in rows);n=sum(r[mode]['characters']for r in rows);agg[mode]={'edits':e,'characters':n,'cer':e/n}
   panels[name]={'units':len(rows),'input_images':sum(len(r['input_ids'])for r in rows),'mode_in_historical_report':panel['mode'],'notes':panel['notes'],'failures':failures,'aggregate':agg,'rows':rows}
  results[engine]={'settings':settings,'distinct_inference_tasks':len(records),'total_inference_seconds':sum(r['seconds']for r in records.values()),'statuses':dict(collections.Counter(r['status']for r in records.values())),'panels':panels}
 out={'date':'2026-11-14','normalization':{'literal':'NFC; whitespace collapsed; case/punctuation retained','reading':'NFC; casefold; Unicode punctuation removed; whitespace collapsed; ё retained'},'labels_not_given_to_engines':True,'scope_adapters':'Known L09 instruction: lowest detected text line only. Frozen page6 final uncertain ink excluded by image rectangle [1560,2540,2150,2765] after recognition; all raw detections retained. No text correction or selection against gold.','results':results}
 (ROOT/'metrics.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 # Matched populations from every standalone-skill row, including incomplete model subsets.
 repo=ROOT.parents[1]/'outputs/handwriting-reference-library';old=json.load(open(repo/'research/evaluations/two-standalone-skills/metrics.json'));matched=[]
 for model,run in old['runs'].items():
  for coll,comparisons in run['comparisons'].items():
   for name,c in comparisons.items():
    if not c:continue
    ids=c['matched_targets'];entry={'reader':model,'collection':coll,'comparison':name,'matched_targets':ids,'engines':{}}
    for engine in results:
     rr=[by_unit[engine]['two-'+i]for i in ids];e=sum(r['reading']['edits']for r in rr);n=sum(r['reading']['characters']for r in rr);entry['engines'][engine]={'edits':e,'characters':n,'cer':e/n}
    matched.append(entry)
 (ROOT/'matched-populations.json').write_text(json.dumps(matched,ensure_ascii=False,indent=2))
 for p in results['tesseract']['panels']:
  print(p,[(e,round(results[e]['panels'][p]['aggregate'][results[e]['panels'][p]['mode_in_historical_report']]['cer']*100,2))for e in results])
if __name__=='__main__':main()
