#!/usr/bin/env python3
"""Ask a local Ollama vision model to review an image; never edit library labels."""
import argparse,base64,hashlib,json,urllib.request
from datetime import datetime,timezone
from pathlib import Path

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--model',required=True,help='An installed model that accepts images')
 ap.add_argument('--image',required=True,type=Path)
 ap.add_argument('--library',type=Path,help='Extracted diary-handwriting-library folder, needed for --reference')
 ap.add_argument('--reference',action='append',default=[],help='Verified crop ID, repeat to supply examples')
 ap.add_argument('--output',required=True,type=Path,help='New JSON file; existing files are never overwritten')
 ap.add_argument('--url',default='http://localhost:11434/api/generate')
 ap.add_argument('--dry-run',action='store_true',help='Write a request summary without contacting Ollama')
 ap.add_argument('--no-think',action='store_true',help='Disable thinking for models that support the think parameter')
 args=ap.parse_args()
 if len(args.reference)>4:ap.error('Use at most four verified references per request.')
 if args.reference and not args.library:ap.error('--reference requires --library')
 if args.output.exists():ap.error('--output must be a new file')
 image=args.image.resolve();raw=image.read_bytes();images=[base64.b64encode(raw).decode()]
 refs=[]
 if args.reference:
  library=args.library.resolve();rows=json.loads((library/'index.json').read_text())['entries'];byid={r['id']:r for r in rows}
  for ident in args.reference:
   if ident not in byid:ap.error('Unknown reference: '+ident)
   r=byid[ident]
   if r['category']!='verified':ap.error('Reference must be user-verified: '+ident)
   p=(library/r['crop_path']).resolve()
   if not p.is_relative_to(library):ap.error('Reference path leaves library')
   data=p.read_bytes()
   if hashlib.sha256(data).hexdigest()!=r['crop_sha256']:ap.error('Reference hash mismatch: '+ident)
   images.append(base64.b64encode(data).decode());refs.append({'id':ident,'label':r['label']})
 skill=(Path(__file__).parent/'SKILL.md').read_text(encoding='utf-8')
 prompt='Image 1 is the target manuscript crop. Read only visible writing in image 1. Return JSON with reading, uncertain_spans, visible_features, and reasons. Use [unclear] for ambiguous parts. Do not repair grammar or infer missing strokes. This is a proposed reading, never a user-verified label. Describe only visible features; agreement with a reference is not proof. '
 for i,r in enumerate(refs,2):prompt+=f'Image {i} is a user-verified reference labeled {r["label"]!r} ({r["id"]}); its label applies only to that image. '
 payload={'model':args.model,'system':skill,'prompt':prompt,'images':images,'stream':False,'format':'json','options':{'temperature':0}}
 if args.no_think:payload['think']=False
 record={'status':'dry_run' if args.dry_run else 'model_suggestion_only','created_at':datetime.now(timezone.utc).isoformat(),'target':str(image),'target_sha256':hashlib.sha256(raw).hexdigest(),'model':args.model,'references':refs,'image_count':len(images),'verified_labels_modified':False}
 if not args.dry_run:
  req=urllib.request.Request(args.url,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST')
  with urllib.request.urlopen(req,timeout=600) as response:record['ollama_response']=json.load(response)
  result=record['ollama_response']
  if not result.get('response','').strip() or result.get('done_reason')=='length':
   record['status']='incomplete_model_output'
   record['review_note']='No complete reading returned. Do not use this response as a label.'
 else:record['request_summary']={'model':args.model,'stream':False,'format':'json','images':len(images),'system_instructions_loaded':True}
 args.output.parent.mkdir(parents=True,exist_ok=True)
 with args.output.open('x',encoding='utf-8') as out:json.dump(record,out,ensure_ascii=False,indent=2)
 print('Written:',args.output)
if __name__=='__main__':main()
