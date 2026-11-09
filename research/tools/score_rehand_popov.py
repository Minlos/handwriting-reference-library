"""Score saved full-page Rehand boxes on the fixed Popov excerpt scopes; no API calls."""
from pathlib import Path
import argparse,json,hashlib,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'handoffs/skill-reference-evaluation'))
from cer import score
from PIL import Image

def select_boxes(boxes,region,scale):
 x0,y0,x1,y1=region;sx,sy=scale
 return [(i,b) for i,b in enumerate(boxes) if x0<=(b['x']+b['w']/2)*sx<x1 and y0<=(b['y']+b['h']/2)*sy<y1]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--letters-dir',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 repo=Path(__file__).resolve().parents[2];fixture=repo/'skills/read-handwriting/test-material/popov';targets=json.loads((fixture/'targets.json').read_text());gold=json.loads((fixture/'evaluator/answers.json').read_text());rows=[]
 for t in targets:
  n=int(t['source_id'].split('-I')[1]);record_path=args.letters_dir/'ocr/rehand'/f'{n:02d}.json';record=json.loads(record_path.read_text());source=args.letters_dir/record['input_file'];digest=hashlib.sha256(source.read_bytes()).hexdigest();assert digest==record['input_sha256'];assert record['status']=='completed'
  with Image.open(source) as im:width,height=im.size
  assert width*2400==height*1800
  roi=t['bbox_xyxy'][:]
  if t['id']=='L09':roi[1]=(roi[1]+roi[3])/2 # Bottom complete line only; the upper clipped line is outside the task.
  chosen=select_boxes(record['response']['boxes'],roi,(1800/width,2400/height))
  text=' '.join(b['text'] for _,b in chosen)
  rows.append({'id':t['id'],'status':'completed','source_input_sha256':digest,'saved_record_sha256':hashlib.sha256(record_path.read_bytes()).hexdigest(),'rehand_input_size':[width,height],'scope_image_size':[1800,2400],'scoring_region_xyxy':roi,'box_indices':[i for i,_ in chosen],'selected_boxes':[b for _,b in chosen],'transcription':text,'reference':gold[t['id']],'reading':score(gold[t['id']],text,'reading'),'literal':score(gold[t['id']],text,'literal')})
 edits=sum(r['reading']['edits'] for r in rows);count=sum(r['reading']['reference_characters'] for r in rows)
 result={'scope':'Same three resolved Popov excerpt scopes; historical full-page OCR, not a matched crop-input rerun','method':'Select box centers geometrically, retain original provider box order. No confidence filtering, text correction or gold-driven matching. L09 excludes partial neighboring line.','normalization':'Same CER function as the two-skill pilot: NFC, case/punctuation ignored, whitespace collapsed, ё distinct.','api_calls':0,'rows':rows,'aggregate':{'edits':edits,'reference_characters':count,'cer':edits/count}}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 for r in rows:print(r['id'],r['reading']['edits'],r['reading']['reference_characters'],round(r['reading']['cer']*100,2),r['transcription'])
 print('TOTAL',edits,count,round(edits/count*100,2))
if __name__=='__main__':main()
