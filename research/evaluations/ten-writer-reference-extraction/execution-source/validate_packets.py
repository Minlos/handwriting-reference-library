from pathlib import Path
import json, hashlib
from PIL import Image,ImageChops
R=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
for f in sorted((R/'packets').glob('writer*/*/packet.json')):
 d=f.parent;m=json.loads(f.read_text());w=int(d.parent.name.removeprefix('writer'));arm=d.name
 sources={p['id']:p for p in json.loads((R/'groups'/f'writer{w:03}'/'sources.json').read_text())['pages']}
 coverage=json.loads((d/'extraction-log.json').read_text())['coverage']
 assert {x.get('source_id',x.get('id')) for x in coverage}==set(sources),(f,'missing source coverage')
 for x in coverage:
  src=sources[x.get('source_id',x.get('id'))];assert x.get('source_sha256',x.get('sha256'))==src['sha256']
 for e in m['examples']:
  src=sources[e['source_id']];assert h(Path(src['path']))==src['sha256']==e['source_sha256']
  crop=d/e.get('crop',e.get('crop_path'));assert h(crop)==e['crop_sha256']
  expected=Image.open(src['path']).convert('RGB').crop(e.get('xyxy',e.get('crop_xyxy')));actual=Image.open(crop).convert('RGB')
  assert expected.size==actual.size and ImageChops.difference(expected,actual).getbbox() is None,(f,e['id'])
  assert e.get('label_status',e.get('status')) in ['provisional','dataset-assisted-provisional']
 assert len(m['examples'])<=24
 sheet=d/'sheet.jpg';im=Image.open(sheet);assert im.width<=1600 and im.height<=2400 and sheet.stat().st_size<=1048576
 labels=[dict(id=e['id'],label=e['label'],label_status=e.get('label_status',e.get('status')),alternatives=e.get('alternatives',[])) for e in m['examples']]
 lp=d/'reader-labels.json';encoded=json.dumps(labels,ensure_ascii=False,indent=2)+'\n'
 if lp.exists():assert lp.read_text()==encoded
 else:lp.write_text(encoded)
 rec=dict(writer=w,arm=arm,crops=len(labels),native_pixel_validation='passed',sheet_sha256=h(sheet),labels_sha256=h(lp),packet_sha256=h(f),sheet_size=sheet.stat().st_size,sheet_dimensions=list(im.size))
 freeze=d/'freeze.json'
 if freeze.exists():assert json.loads(freeze.read_text())==rec
 else:freeze.write_text(json.dumps(rec,indent=2)+'\n')
 results.append(rec)
(R/'packet-validation.json').write_text(json.dumps(results,indent=2)+'\n')
print('Validated',len(results),'packets;',sum(x['crops'] for x in results),'exact native-pixel crops')
