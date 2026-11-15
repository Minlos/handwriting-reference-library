from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();records=[]
for model in ['astra','sol']:
 for p in sorted((R/'predictions'/model).glob('*/rep*/writer*.json')):
  if '-raw-' in p.name:continue
  d=json.loads(p.read_text());w=d['writer'];c=d['condition'];rep=d['replicate'];task=json.loads((R/'reader-tasks'/model/c/f'rep{rep}'/f'writer{w:03}.json').read_text());assert d['model']==task['model'] and d['no_skill'] and d['prompt_sha256']==task['prompt_sha256']
  assert d['status'] in ['completed','error'];expected=[x['id'] for x in task['targets']]
  if d['status']=='completed':assert [x['id'] for x in d['pages']]==expected and all(isinstance(x['prediction'],str) and x['prediction'].strip() for x in d['pages'])
  assert [x['id'] for x in d['coverage']]==expected
  assert all(1<=x['original_requests']<=3 for x in d['coverage'])
  if c!='A':
   freeze=json.loads((R/'packets'/f'writer{w:03}'/c/'freeze.json').read_text());refs=d.get('reference_hashes',d.get('reference',dict(sheet_sha256=d.get('reference_sheet_sha256',d.get('sheet_sha256')),labels_sha256=d.get('reference_labels_sha256',d.get('labels_sha256')))));assert refs['sheet_sha256']==freeze['sheet_sha256'] and refs['labels_sha256']==freeze['labels_sha256']
  raw=[p.parent/f'writer{w:03}-raw-{v}.json' for v in ['initial','final']];assert all(x.exists() for x in raw)
  records.append(dict(file=str(p.relative_to(R)),sha256=H(p),raw_sha256={x.name:H(x) for x in raw},writer=w,condition=c,replicate=rep,model=model,status=d['status'],coverage=d['coverage']))
previous=R/'prediction-validation.json'
if previous.exists():
 old={x['file']:x for x in json.loads(previous.read_text())};new={x['file']:x for x in records}
 for k,x in old.items():assert k in new and x['sha256']==new[k]['sha256'] and x['raw_sha256']==new[k]['raw_sha256'],('Previously frozen prediction/raw changed',k)
(R/'prediction-validation.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');print('Validated',len(records),'Astra/Sol documents; input/ref hashes, page IDs, actual request budgets, raw files checked.')
