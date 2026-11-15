"""Fresh independent API calls; budget helper owns locked reservations; no paid retries."""
from pathlib import Path
import json,hashlib,importlib.util,time,argparse,math
from portable_paths import resolve
R=Path(__file__).resolve().parent;W=R.parents[1]
spec=importlib.util.spec_from_file_location('budget_api',R/'provider_api.py');api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
PROMPT=(R/'reader-prompt.txt').read_text();OUT=R/'deepseek-replay';OUT.mkdir(exist_ok=True)
def run(w,c,rep,key):
 stem=f'writer{w:03}-{c}-rep{rep}';dest=OUT/(stem+'.json')
 if dest.exists():return
 pages=json.loads((R/'groups'/f'writer{w:03}'/'targets.json').read_text())['pages'];parts=[];records=[]
 if c!='A':
  d=R/'packets'/f'writer{w:03}'/c;freeze=json.loads((d/'freeze.json').read_text());sheet=d/'sheet.jpg';lp=d/'reader-labels.json'
  assert H(sheet)==freeze['sheet_sha256'] and H(lp)==freeze['labels_sha256']
  parts=[('text','REFERENCE contact sheet and provisional labels: '+lp.read_text()),('image',sheet)]
  records.append(dict(role='reference',sheet_sha256=H(sheet),labels_sha256=H(lp)))
 for p in pages:
  path=resolve(R,p['path']);assert H(path)==p['sha256'];parts += [('text','TARGET '+p['id']),('image',path)];records.append(dict(role='target',id=p['id'],sha256=p['sha256']))
 # Serialize exactly the helper's payload only in memory, never persist base64 or credentials.
 body=api.content(parts,'deepseek');payload=dict(model=api.MODELS['deepseek'],messages=[{'role':'system','content':PROMPT},{'role':'user','content':body}],thinking={'type':'disabled'},temperature=0,max_tokens=api.MAX_OUTPUT,stream=False)
 size=len(json.dumps(payload).encode());del payload,body
 assert size<48*1048576,('Request body exceeds frozen inline limit',size)
 meta=dict(writer=w,condition=c,replicate=rep,model='deepseek-flash',no_skill=True,inputs=records,prompt_sha256=H(R/'reader-prompt.txt'),payload_bytes=size,original_target_presentations=1,reference_presentations=int(c!='A'),host_difference='Single independent API request; no dynamic image reinspection')
 (OUT/(stem+'-inputs.json')).write_text(json.dumps(meta,indent=2)+'\n')
 call='replay-'+stem;api.reserve('deepseek',call);start=time.monotonic();cost=None
 try:
  response=api.request('deepseek',key,PROMPT,parts);text,complete,cost=api.extract('deepseek',response)
  rec=dict(**meta,status='received',response_model=response.get('model'),usage=response.get('usage'),finish_reason=response['choices'][0].get('finish_reason'),content=text,cost_upper_usd=cost,seconds=time.monotonic()-start)
  dest.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
  raw=OUT/(stem+'-raw-received.json');assert not raw.exists();raw.write_bytes(dest.read_bytes())
  assert complete,'Incomplete API response'
  decoded=json.loads(text);results=decoded['pages'];assert [x['id'] for x in results]==[p['id'] for p in pages]
  for p,x in zip(pages,results):assert isinstance(x['prediction'],str) and x['prediction'].strip()
  pred=OUT/'predictions'/'deepseek'/c/f'rep{rep}'/f'writer{w:03}.json';pred.parent.mkdir(parents=True,exist_ok=True);assert not pred.exists()
  pred.write_text(json.dumps(dict(**meta,status='completed',pages=results,response_model=response.get('model'),raw_sha256=H(raw),raw_file=raw.name),ensure_ascii=False,indent=2)+'\n')
  rec['status']='completed';dest.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');api.settle(call,cost,'complete');print(stem,'completed',cost,flush=True)
 except Exception as e:
  rec=json.loads(dest.read_text()) if dest.exists() else meta.copy();rec.update(status='error',error=type(e).__name__+': '+str(e)[:200],seconds=time.monotonic()-start);dest.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');api.settle(call,cost,'error_unknown_billing' if cost is None else 'error_response');print(stem,'error',type(e).__name__,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');p.add_argument('--writers',default='17,18,20,21,22,23,24,25,26,28');p.add_argument('--rep',type=int,default=1);a=p.parse_args();
 if not a.execute:p.error('Paid replay requires --execute plus a separately approved local replay budget')
 assert (R/'evaluator'/'audit-freeze.json').exists()
 if a.rep==2:
  assert all((OUT/f'writer{w:03}-{c}-rep1.json').exists() for w in [17,18,20,21,22,23,24,25,26,28] for c in 'ABC'),'Replicate1 across all writers must precede2'
 key=api.credential('deepseek')
 for w in map(int,a.writers.split(',')):
  for c in 'ABC':
   try:run(w,c,a.rep,key)
   except RuntimeError as e:
    if 'budget' in str(e).lower() or 'Spending approval insufficient' in str(e):print('HARD STOP: existing shared budget cannot cover next reservation',flush=True);raise SystemExit(0)
    raise
