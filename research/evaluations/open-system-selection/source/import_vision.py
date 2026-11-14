from pathlib import Path
import json
r=Path(__file__).resolve().parent;out=r/'apple-vision';out.mkdir(exist_ok=True)
for s in json.loads((r/'inputs.json').read_text())['items']:
 path=r/'apple-vision-raw'/(s['id']+'.json')
 if not path.exists():continue
 x=json.loads(path.read_text());selected=x.get('selected',{});rec={'id':s['id'],'input_sha256':s['sha256'],'raw':x,'engine':'Apple Vision accurate CPU, ru-RU/en-US, correction disabled, upright original'}
 if 'error'in selected:rec.update(status='error',error=selected['error'])
 else:rec.update(status='completed',prediction='\n'.join(v['text']for v in selected.get('lines',[])))
 (out/(s['id']+'.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2))
