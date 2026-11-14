"""Local conventional OCR inference. Reads only inputs.json, never evaluator references."""
from pathlib import Path
import argparse,json,hashlib,time,subprocess,os,csv,io,collections,importlib.metadata
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2));tmp.replace(p)
def select(lines,scope):
 if scope=='bottom-line'and lines:
  y=max(x['cy']for x in lines);h=max(x['height']for x in lines);lines=[x for x in lines if x['cy']>=y-.5*h];lines.sort(key=lambda x:x['x'])
 return '\n'.join(x['text']for x in lines)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--engine',choices=['tesseract','easyocr'],required=True);a=ap.parse_args();out=ROOT/a.engine;out.mkdir(exist_ok=True);specs=json.load(open(ROOT/'inputs.json'))['items']
 if a.engine=='tesseract':
  exe='/opt/homebrew/bin/tesseract';weights=BASE/'work/ocr-models/tesseract';settings={'engine':a.engine,'version':subprocess.check_output([exe,'--version'],text=True).splitlines()[0],'language':'rus','rus_traineddata_sha256':sha(weights/'rus.traineddata'),'model_family':'official tessdata_best Russian LSTM','oem':1,'page_psm':3,'single_line_psm':7,'threads':2,'output_format':'explicit tessedit_create_tsv=1'}
 else:
  import torch,easyocr,numpy as np
  from PIL import Image
  torch.set_num_threads(2);torch.manual_seed(20261114);models=BASE/'work/ocr-models/easyocr';reader=easyocr.Reader(['ru','en'],gpu=False,model_storage_directory=str(models),user_network_directory=str(models/'user'),download_enabled=False,verbose=False)
  settings={'engine':a.engine,'version':importlib.metadata.version('easyocr'),'torch_version':torch.__version__,'languages':['ru','en'],'gpu':False,'decoder':'greedy','canvas_size':2560,'workers':0,'paragraph':False,'recognition_model':'cyrillic_g2','model_sha256':{f.name:sha(f)for f in models.glob('*.pth')},'threads':2,'seed':20261114}
 fingerprint=hashlib.sha256(json.dumps(settings,sort_keys=True).encode()).hexdigest();write(out/'settings.json',settings)
 for n,spec in enumerate(specs):
  p=Path(spec['path']);assert sha(p)==spec['sha256'];dest=out/'records'/(spec['id']+'.json')
  if dest.exists():assert json.load(open(dest))['settings_sha256']==fingerprint;continue
  record={'id':spec['id'],'input_sha256':spec['sha256'],'settings_sha256':fingerprint,'scope_adapter':spec['scope'],'status':'running'};start=time.monotonic()
  try:
   if a.engine=='tesseract':
    args=[exe,str(p),'stdout','--tessdata-dir',str(weights),'-l','rus','--oem','1','--psm','7'if spec['line']else'3','-c','tessedit_create_tsv=1'];r=subprocess.run(args,text=True,capture_output=True,timeout=180,env={**os.environ,'OMP_THREAD_LIMIT':'2'})
    if r.returncode:raise RuntimeError(r.stderr[-1000:])
    raw=r.stdout;assert raw.startswith('level\tpage_num\t'),'Engine did not return TSV';groups=collections.OrderedDict()
    for w in csv.DictReader(io.StringIO(raw),delimiter='\t',quoting=csv.QUOTE_NONE):
     if not w['text'].strip():continue
     k=tuple(w[x]for x in ['page_num','block_num','par_num','line_num']);groups.setdefault(k,[]).append(w)
    lines=[]
    for ws in groups.values():
     top=min(int(w['top'])for w in ws);bottom=max(int(w['top'])+int(w['height'])for w in ws);lines.append({'text':' '.join(w['text']for w in ws),'cy':(top+bottom)/2,'height':bottom-top,'x':min(int(w['left'])for w in ws)})
   else:
    im=Image.open(p).convert('RGB');arr=np.array(im)
    if spec['line']:raw=reader.recognize(np.array(im.convert('L')),horizontal_list=[[0,im.width,0,im.height]],free_list=[],detail=1,decoder='greedy',paragraph=False,batch_size=1,workers=0)
    else:raw=reader.readtext(arr,detail=1,decoder='greedy',paragraph=False,batch_size=1,workers=0,canvas_size=2560)
    raw=[{'box':[[float(x),float(y)]for x,y in box],'text':str(t),'confidence':float(c)}for box,t,c in raw];lines=[]
    for r in raw:
     ys=[p[1]for p in r['box']];lines.append({'text':r['text'],'cy':sum(ys)/len(ys),'height':max(ys)-min(ys),'x':min(p[0]for p in r['box'])})
   record.update(status='completed',prediction=select(lines,spec['scope']),raw=raw,detected_lines=lines)
  except Exception as exc:record.update(status='error',error_type=type(exc).__name__,error=str(exc)[:1000])
  record['seconds']=time.monotonic()-start;write(dest,record);print(a.engine,n+1,'/',len(specs),spec['id'],record['status'],round(record['seconds'],2),flush=True)
 print('FINISHED',a.engine,flush=True)
if __name__=='__main__':main()
