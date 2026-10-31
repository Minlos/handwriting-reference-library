"""Validate source hashes, crop coordinates, pixels, paths, and categories."""
from pathlib import Path
import json,hashlib,sys
from PIL import Image,ImageChops
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
manifest=json.loads((root/'source-manifest.json').read_text())
entries=json.loads((root/'index.json').read_text())['entries']
sources={s['source_filename']:s for s in manifest}
for s in manifest:
 p=root/s['source_path']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'],p
 with Image.open(p) as im:assert list(im.size)==[s['width'],s['height']]
assert len({r['id'] for r in entries})==len(entries)
for r in entries:
 assert r['category'] in ['verified','provisional']
 p=root/r['crop_path'];s=sources[r['source_filename']]
 assert hashlib.sha256(p.read_bytes()).hexdigest()==r['crop_sha256'],p
 assert 0<=r['x0']<r['x1']<=s['width'] and 0<=r['y0']<r['y1']<=s['height']
 with Image.open(root/s['source_path']) as im:
  expected=im.crop(tuple(r[k] for k in ['x0','y0','x1','y1'])).rotate(r['rotation_ccw'],expand=True).convert('RGB')
  with Image.open(p) as saved:
   assert expected.size==saved.size,(r['id'],expected.size,saved.size)
   assert ImageChops.difference(expected,saved.convert('RGB')).getbbox() is None,r['id']
passage_index=root/'reread/passage-index.json'
passage_count=0
if passage_index.exists():
 for r in json.loads(passage_index.read_text()):
  p=root/r['crop_path'];s=sources[r['source_filename']]
  assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],p
  with Image.open(root/s['source_path']) as im:
   expected=im.crop(tuple(r[k] for k in ['x0','y0','x1','y1'])).rotate(r['rotation_ccw'],expand=True).convert('RGB')
   with Image.open(p) as saved:
    assert expected.size==saved.size
    assert ImageChops.difference(expected,saved.convert('RGB')).getbbox() is None,r['id']
  passage_count+=1
print(f'PASS: {len(manifest)} original hashes; {len(entries)} library crops and {passage_count} passage crops reproduce original pixels exactly.')
