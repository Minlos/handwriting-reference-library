"""Preserve byte-exact received-state records hashed by initial parser before status update.
Legacy runner saved content immutably but updated record status after parsing. Reconstruct only
that explicit status field, verify saved prediction hash, and preserve alongside final summary.
No prediction or final API record is modified.
"""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;log=[]
for p in sorted((R/'predictions'/'deepseek').glob('*/rep*/writer*.json')):
 m=json.loads(p.read_text());stem=f'writer{m["writer"]:03}-{m["condition"]}-rep{m["replicate"]}';summary=R/'deepseek-api'/(stem+'.json');raw=R/'deepseek-api'/(stem+'-raw-received.json')
 if not raw.exists():
  data=json.loads(summary.read_text());assert data['status']=='completed';data['status']='received';b=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode();assert hashlib.sha256(b).hexdigest()==m['raw_sha256'];raw.write_bytes(b);log.append(dict(file=raw.name,provenance='Byte-exact reconstruction of pre-status-update record, independently matched to hash in immutable parsed prediction. Content unchanged.'))
 assert hashlib.sha256(raw.read_bytes()).hexdigest()==m['raw_sha256']
if log:
 out=R/'api-raw-preservation.json';existing=json.loads(out.read_text()) if out.exists() else [];out.write_text(json.dumps(existing+log,indent=2)+'\n')
print('Verified',len(list((R/'predictions'/'deepseek').glob('*/rep*/writer*.json'))),'raw received record hashes')
