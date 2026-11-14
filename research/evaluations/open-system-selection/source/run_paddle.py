from pathlib import Path
import os,json,time,hashlib,importlib.metadata
R=Path(__file__).resolve().parent;B=R.parents[1]
os.environ['PADDLE_PDX_CACHE_HOME']=str(B/'work/ocr-models/paddlex');os.environ['PADDLE_HOME']=str(B/'work/ocr-models/paddle');os.environ['HF_HOME']=str(B/'work/runtime-cache/huggingface');os.environ['PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK']='True'
from paddleocr import PaddleOCR
out=R/'paddleocr';out.mkdir(exist_ok=True)
settings={'paddleocr':importlib.metadata.version('paddleocr'),'paddlepaddle':importlib.metadata.version('paddlepaddle'),'lang':'ru','ocr_version':'PP-OCRv5','device':'cpu','use_doc_orientation_classify':False,'use_doc_unwarping':False,'use_textline_orientation':False}
(out/'settings.json').write_text(json.dumps(settings,indent=2))
ocr=PaddleOCR(lang='ru',ocr_version='PP-OCRv5',device='cpu',use_doc_orientation_classify=False,use_doc_unwarping=False,use_textline_orientation=False,enable_mkldnn=False,cpu_threads=2)
for s in json.loads((R/'inputs.json').read_text())['items']:
 dest=out/(s['id']+'.json')
 if dest.exists():continue
 assert hashlib.sha256(Path(s['path']).read_bytes()).hexdigest()==s['sha256'];rec={'id':s['id'],'input_sha256':s['sha256'],'status':'running'};start=time.monotonic()
 try:
  rr=[]
  for result in ocr.predict(s['path']):
   x=result.json;rr.append(x if isinstance(x,dict)else json.loads(x))
  rec.update(status='completed',raw=rr,prediction='\n'.join(t for x in rr for t in x.get('res',x).get('rec_texts',[])))
 except Exception as e:rec.update(status='error',error=str(e)[:500])
 rec['seconds']=time.monotonic()-start;dest.write_text(json.dumps(rec,ensure_ascii=False,indent=2));print('PaddleOCR',s['id'],rec['status'],flush=True)
