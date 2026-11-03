#!/usr/bin/env python3
"""Evaluator-only scoring for a complete four-condition matrix, including recorded failures."""
from pathlib import Path
import argparse,json,re,hashlib,unicodedata
from cer import score,normalize,distance
HERE=Path(__file__).resolve().parent
KEYS=['setup','model','trial','condition','page']
def key(r):return tuple(r[k] for k in KEYS)
def lines(p):return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]
def clean(s):
 s=''.join(c for c in s if unicodedata.category(c)!='Cf');s=re.sub(r'\[(?:неразборчиво|unclear|illegible|зачеркнуто)[^\]]*\]','',s,flags=re.I);return re.sub(r'\[([^\]]+)\?\]',r'\1',s)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--predictions',type=Path,required=True);ap.add_argument('--exclusions',type=Path);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();rows=lines(args.predictions);masks={key(r):r for r in lines(args.exclusions)} if args.exclusions else {};protocol=json.loads((HERE/'protocol.json').read_text());gold={}
 if len({key(r) for r in rows})!=len(rows):raise ValueError('Duplicate primary result; put recovery attempts in a separate file')
 for t in protocol['targets']:
  raw=(HERE/t['gold_file']).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=t['gold_sha256']:raise ValueError('Frozen gold hash mismatch')
  gold[t['page']]=raw.decode()
 output={'protocol_sha256':hashlib.sha256((HERE/'protocol.json').read_bytes()).hexdigest(),'normalization':'NFC, whitespace collapsed; reading CER ignores case/punctuation, retains ё/е distinction. Unknown markers on known text count as omissions. Default six targets have no excluded words; an explicit page-6 suffix mask is required only for a future protocol that targets page 6.','rows':[],'groups':[]}
 for r in rows:
  if r['condition'] not in 'ABCD' or len(r['condition'])!=1 or r['page'] not in gold:raise ValueError('Invalid condition or target')
  item={k:r[k] for k in KEYS};item['status']=r['status']
  if r['status']=='completed':
   h=r.get('transcription')
   if not isinstance(h,str) or not h.strip():raise ValueError('Completed row must contain a nonempty transcription')
   if r['page']==6:
    mask=masks.get(key(r),{});suffix=mask.get('excluded_suffix')
    if not suffix or not mask.get('basis') or not h.endswith(suffix):raise ValueError('Manually reviewed exact page-6 suffix and basis required')
    h=h[:-len(suffix)];item['excluded_suffix']=suffix
   ref,h=clean(gold[r['page']]),clean(h)
   for mode in ['literal','reading']:item[mode]=score(ref,h,mode)
   a,b=normalize(ref,'reading').split(),normalize(h,'reading').split();item['word']={'edits':distance(a,b),'reference_words':len(a),'wer':distance(a,b)/len(a)}
  output['rows'].append(item)
 for setup,model,trial in sorted({(r['setup'],r['model'],r['trial']) for r in rows}):
  group={'setup':setup,'model':model,'trial':trial,'conditions':{},'relative_error_reduction':{}}
  for c in 'ABCD':
   rr=[r for r in output['rows'] if (r['setup'],r['model'],r['trial'],r['condition'])==(setup,model,trial,c)];good=[r for r in rr if 'reading' in r];entry={'completed_pages':[r['page'] for r in good],'primary_statuses':{str(r['page']):r['status'] for r in rr},'aggregate':None}
   if {r['page'] for r in good}==set(gold):
    entry['aggregate']={}
    for mode in ['literal','reading']:
     e=sum(r[mode]['edits'] for r in good);n=sum(r[mode]['reference_characters'] for r in good);entry['aggregate'][mode]={'edits':e,'reference_characters':n,'cer':e/n}
   group['conditions'][c]=entry
  for label,a,b in [('skill_without_references','A','B'),('skill_with_references','C','D'),('references_without_skill','A','C'),('references_with_skill','B','D'),('joint_skill_and_references','A','D')]:
   aa,bb=group['conditions'][a]['aggregate'],group['conditions'][b]['aggregate'];group['relative_error_reduction'][label]=None if not aa or not bb or not aa['reading']['cer'] else 1-bb['reading']['cer']/aa['reading']['cer']
  output['groups'].append(group)
 with args.output.open('x') as f:json.dump(output,f,ensure_ascii=False,indent=2)
 print('Saved',args.output,'; missing/failed conditions have no complete-page aggregate.')
if __name__=='__main__':main()
