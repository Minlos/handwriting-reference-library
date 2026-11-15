from pathlib import Path
from portable_paths import resolve
import json,sys,time,math,hashlib,os
BASE=Path.cwd();ROOT=Path(__file__).resolve().parent;os.environ['NO_ALBUMENTATIONS_UPDATE']='1';os.environ['MPLCONFIGDIR']=str(BASE/'work/runtime-cache/matplotlib');sys.path.insert(0,str(ROOT))
from recognizer_crnn import Recognizer
from PIL import Image
import torch
from kraken import blla
from kraken.tasks import RecognitionTaskModel
from kraken.configs import RecognitionInferenceConfig
from kraken.containers import Segmentation,BBoxLine
from importlib import resources
items=json.loads((ROOT/'inputs.json').read_text())['items'];torch.set_num_threads(2)
settings=json.loads((ROOT/'baseline-settings.json').read_text());assert hashlib.sha256((ROOT/'russian-crnn.pt').read_bytes()).hexdigest()==settings['weights']['work/ocr-models/russian-crnn.pt']['sha256'];assert hashlib.sha256(resources.files('kraken').joinpath('blla.mlmodel').read_bytes()).hexdigest()==settings['segmentation_sha256']
models={'russian-crnn':Recognizer(str(ROOT/'russian-crnn.pt'))}
lineout=ROOT/'baseline-replay'/'line-crops';lineout.mkdir(parents=True,exist_ok=True)
for s in items:
 p=resolve(ROOT,s['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'];im=Image.open(p).convert('RGB');start=time.monotonic();seg=blla.segment(im,device='cpu');boxes=[];crops=[]
 for i,line in enumerate(seg.lines):
  if not line.boundary:continue
  pts=line.boundary;box=(max(0,math.floor(min(v[0]for v in pts))),max(0,math.floor(min(v[1]for v in pts))),min(im.width,math.ceil(max(v[0]for v in pts))),min(im.height,math.ceil(max(v[1]for v in pts))))
  if box[2]<=box[0]or box[3]<=box[1]:continue
  ident=f'{s["id"]}-{i:03}';cp=lineout/(ident+'.png');im.crop(box).save(cp);crops.append(cp);boxes.append(BBoxLine(id=ident,bbox=box))
 segseconds=time.monotonic()-start;bounds=Segmentation(type='bbox',imagename=str(p),text_direction='horizontal-lr',script_detection=False,lines=boxes)
 for engine,model in models.items():
  out=ROOT/'baseline-replay'/engine;out.mkdir(parents=True,exist_ok=True);dest=out/(s['id']+'.json')
  if dest.exists():continue
  rec={'id':s['id'],'input_sha256':s['sha256'],'scope':'all','segmentation_seconds':segseconds,'line_boxes':[list(b.bbox)for b in boxes],'status':'running'};start=time.monotonic()
  try:
   if not boxes:raise RuntimeError('No lines detected')
   pred=[model.read(cp)for cp in crops]if engine=='russian-crnn'else[r.prediction for r in model.predict(im,bounds,RecognitionInferenceConfig(accelerator='cpu',device='auto',num_line_workers=0,bidi_reordering=False))]
   rec.update(status='completed',prediction='\n'.join(pred),line_predictions=pred)
  except Exception as e:rec.update(status='error',error=str(e)[:400])
  rec['seconds']=time.monotonic()-start;dest.write_text(json.dumps(rec,ensure_ascii=False,indent=2));print(engine,s['id'],rec['status'],len(boxes),'lines',flush=True)
