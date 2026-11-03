#!/usr/bin/env python3
"""Export isolated per-target/condition folders. Never reads evaluator gold. No network."""
from pathlib import Path
from PIL import Image
import argparse,io,json,hashlib,math
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def checked(p,expected):
 raw=p.read_bytes()
 if sha(raw)!=expected:raise ValueError('Hash mismatch: '+p.name)
 return raw
def render():
 protocol=json.loads((HERE/'protocol.json').read_text());skill=checked(HERE/protocol['skill_file'],protocol['skill_sha256']);labels=json.loads(checked(HERE/protocol['reference_labels_file'],protocol['reference_labels_sha256']));assets={}
 for spec in protocol['reference_images']+protocol['targets']:
  raw=checked(REPO/'sources'/spec['source_filename'],spec['source_sha256']);im=Image.open(io.BytesIO(raw)).rotate(spec['rotation_ccw'],expand=True);buf=io.BytesIO()
  if 'upright_box' in spec:
   im=im.crop(tuple(spec['upright_box'])).convert('RGB');pixel=sha(f'RGB:{im.width}x{im.height}:'.encode()+im.tobytes())
   if pixel!=spec['pixel_sha256']:raise ValueError('Target pixels differ from frozen protocol')
   im.save(buf,format='PNG');name=f'target-{spec["page"]:02d}.png'
  else:
   recipe=protocol['reference_image_recipe'];im.thumbnail(tuple(recipe['max_size']));im.save(buf,format='JPEG',quality=recipe['jpeg_quality'],optimize=recipe['optimize']);name=f'reference-{spec["page"]:02d}.jpg'
   # Frozen label boxes are for this exact reference-image coordinate system.
   if im.size!=(1800,2400):raise ValueError('Unexpected reference image dimensions')
  assets[name]=buf.getvalue()
 return protocol,skill,labels,assets

def packet(page,condition,protocol,skill,labels,assets):
 flags=protocol['conditions'][condition];name=f'target-{page:02d}.png';files={name:assets[name]};prompt=(HERE/'base-prompt.txt').read_text();attachments=[name]
 if flags['references']:
  for p in sorted(int(n) for n in labels):
   name=f'reference-{p:02d}.jpg';files[name]=assets[name];attachments.append(name)
  files['reference-labels.json']=json.dumps(labels,ensure_ascii=False,indent=2).encode();prompt+='\nREFERENCE IMAGES: use the three reference JPEGs in this folder and the corrected texts in reference-labels.json. Explicitly unresolved text is not a verified label.\n'
 if flags['skill']:
  files['SKILL.md']=skill;prompt+='\nApply the attached SKILL.md to the permitted inputs only.\n'
 prompt+=f'\nTARGET: target-{page:02d}.png. Transcribe this target only.\n'
 files['task.txt']=prompt.encode();metadata={'condition':condition,'page':page,'flags':flags,'attach_images':attachments,'attach_text_files':(['reference-labels.json'] if flags['references'] else [])+(['SKILL.md'] if flags['skill'] else []),'prompt_file':'task.txt','file_sha256':{k:sha(v) for k,v in files.items()},'note':'Copy only this folder to the model workspace. No answer files, author profile, error log or sibling packets are permitted.'};files['packet.json']=json.dumps(metadata,ensure_ascii=False,indent=2).encode();return files

def main():
 p=argparse.ArgumentParser();mode=p.add_mutually_exclusive_group(required=True);mode.add_argument('--validate-only',action='store_true');mode.add_argument('--output',type=Path);a=p.parse_args();protocol,skill,labels,assets=render()
 if a.output:a.output.mkdir(parents=True,exist_ok=False)
 for page in [t['page'] for t in protocol['targets']]:
  for condition in 'ABCD':
   files=packet(page,condition,protocol,skill,labels,assets)
   if a.output:
    folder=a.output/condition/f'page-{page:02d}';folder.mkdir(parents=True)
    for name,raw in files.items():(folder/name).write_bytes(raw)
 if a.output:(a.output/'EXPORT.json').write_text(json.dumps({'protocol_sha256':sha((HERE/'protocol.json').read_bytes()),'packets':4*len(protocol['targets']),'gold_exported':False,'paid_calls':0},indent=2))
 print('PASS:',4*len(protocol['targets']),'packets; exact target pixels; references only in C/D; skill only in B/D; no gold exported; no API calls.')
if __name__=='__main__':main()
