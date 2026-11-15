from pathlib import Path
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parent;H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hashes={'sources':set(),'targets':set()};counts={};rows=[]
for role in hashes:
 count=0
 for mf in sorted((R/'groups').glob('*/'+role+'.json')):
  for x in json.loads(mf.read_text())['pages']:
   p=Path(x['path']);assert H(p)==x['sha256'];im=Image.open(p);assert list(im.size)==x['dimensions'];im.load();Image.open(p).verify();hashes[role].add(x['sha256']);count+=1;rows.append(dict(id=x['id'],role=role,sha256=x['sha256'],dimensions=x['dimensions']))
 counts[role]=count
assert counts==dict(sources=57,targets=45);assert not hashes['sources']&hashes['targets']
proto=json.loads((R/'protocol.json').read_text())
for name,h in proto['skill_hashes'].items():assert H(R/'skill-snapshots'/name)==h
freeze=json.loads((R/'evaluator'/'audit-freeze.json').read_text());assert H(R/'evaluator'/'preinference-audit.json')==freeze['audit_sha256']
for w,h in freeze['gold_sha256'].items():assert H(R/'evaluator'/'published'/f'writer{int(w):03}.txt')==h
assert H(R/'protocol.json')==json.loads((R/'public-runtime'/'protocol.public.json').read_text())['private_execution_protocol_sha256']
out=dict(counts=counts,cross_role_image_hash_overlap=0,images=rows,frozen_skill_snapshots='all3hashes match protocol',frozen_audit_and_published_gold='unchanged',execution_protocol_sha256=H(R/'protocol.json'),reader_prompt_sha256=H(R/'reader-prompt.txt'))
(R/'final-input-verification.json').write_text(json.dumps(out,indent=2)+'\n');print('Verified102 original decoded image hashes/dimensions, zero cross-role overlaps,3skill snapshots, frozen audit/gold/protocol.')
