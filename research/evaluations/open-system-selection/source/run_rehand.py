from pathlib import Path
import json,hashlib,time,requests
base=Path(__file__).resolve().parent;out=base/'rehand';out.mkdir(exist_ok=True)
items=json.loads((base/'inputs.json').read_text())['items']
for s in items:
 dest=out/(s['id']+'.json')
 if dest.exists():continue
 raw=Path(s['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==s['sha256'];record={'id':s['id'],'input_sha256':s['sha256'],'status':'running','service':'Rehand','input':'identical original bytes; no resizing'};start=time.monotonic()
 try:
  r=requests.post('https://rehand.ru/api/v1/upload',files={'file':(Path(s['path']).name,raw,'image/png'if Path(s['path']).suffix=='.png'else'image/jpeg')},data={'type':'handwriting'},timeout=150);record['http_status']=r.status_code
  if r.status_code!=200:raise RuntimeError('HTTP '+str(r.status_code)+' '+r.text[:150])
  x=r.json();record['response']={k:v for k,v in x.items()if 'image'not in k.lower()};record['prediction']=x.get('output_text')or'\n'.join(str(b.get('text',''))for b in x.get('boxes',[]));record['status']='completed'
 except Exception as e:record.update(status='error',error=str(e)[:300])
 record['seconds']=time.monotonic()-start;dest.write_text(json.dumps(record,ensure_ascii=False,indent=2));print('Rehand',s['id'],record['status'],flush=True)
 if record['status']=='error':break
