from pathlib import Path
import sys,json,hashlib,importlib.util
ROOT=Path.cwd();repo=ROOT/'outputs/handwriting-reference-library';out=ROOT/'work/conventional-baselines';(out/'inputs').mkdir(exist_ok=True)
items={};panels={};gold={}
def add(path,scope='all',line=False):
 path=Path(path).resolve();sha=hashlib.sha256(path.read_bytes()).hexdigest();key=sha[:20]+('-bottom'if scope=='bottom-line'else'')+('-line'if line else'')
 row={'id':key,'path':str(path),'sha256':sha,'scope':scope,'line':line}
 if key in items:assert items[key]==row or (items[key]['sha256']==sha and items[key]['scope']==scope)
 else:items[key]=row
 return key
def panel(name,records,mode='reading',notes=''):
 panels[name]={'records':records,'mode':mode,'notes':notes}
def rec(i,files,ref):gold[name_key:=i]=ref;return {'unit':i,'inputs':files,'gold_id':i}
# Frozen single-line diagnostic.
m=json.load(open(ROOT/'outputs/ocr-evaluation/results/benchmark-manifest.json'))
rr=[]
for r in m['samples']:
 p=ROOT/'outputs/diary-handwriting-library'/r['crop_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['crop_sha256'];rr.append(rec('crop-'+r['id'],[add(p,line=True)],r['label']))
panel('diary-14-crops',rr,notes='Historical hand-selected single-line diagnostic; preserves frozen labels, not representative whole-page accuracy.')
# Exact full-text-region PNGs used by Sol, Gemma and Grok three-page tests.
rr=[]
for page,letter in [(4,'a'),(6,'b'),(7,'c')]:rr.append(rec(f'diary3-P{page:02}',[add(ROOT/f'work/sol-matched-tests-20261102/inputs/scan-{letter}.png')],(ROOT/f'outputs/ocr-evaluation/sol-matched-pages-4-6-7/page-{page:02d}-reference.txt').read_text()))
panel('diary-3-pages',rr,notes='Same exact target bytes as the matched Sol/Gemma/Grok tests. Only final unresolved word of page6 is excluded using the frozen pre-word text boundary; segmentation/scope failures remain scored.')
# Frozen six-page target assets, generated with its original recipe.
spec=importlib.util.spec_from_file_location('preparer',repo/'research/handoffs/skill-reference-evaluation/prepare_inputs.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);protocol,_,_,assets=mod.render();rr=[]
for t in protocol['targets']:
 page=t['page'];p=out/f'inputs/diary6-{page:02}.png';p.write_bytes(assets[f'target-{page:02}.png']);ref=(repo/'research/handoffs/skill-reference-evaluation'/t['gold_file']).read_text();assert hashlib.sha256(ref.encode()).hexdigest()==t['gold_sha256'];rr.append(rec(f'diary6-P{page:02}',[add(p)],ref))
panel('diary-6-pages',rr,notes='Exact original six-page target bytes and evaluator copies; same images as standalone-skill diary panel, checked below.')
# Standalone-skill diary and Popov excerpts.
two=ROOT/'work/two-skill-benchmark';targets=json.load(open(two/'targets/targets.json'));gg=json.load(open(two/'evaluator/gold.json'))
for coll in ['diary','letters']:
 rr=[]
 for t in targets:
  if t['collection']!=coll:continue
  p=two/'targets'/t['image'];assert hashlib.sha256(p.read_bytes()).hexdigest()==t['sha256'];scope='bottom-line'if t['id']=='L09'else'all';rr.append(rec('two-'+t['id'],[add(p,scope=scope)],gg[t['id']]))
 panel('two-skills-'+coll,rr,notes='Exact frozen input bytes. L09 follows its supplied instruction with a fixed geometric adapter: keep only the lowest detected text line, without consulting gold. Raw full-image detections also retained. No target word exclusions.')
# Public dataset comparisons, ordered pages joined before document CER.
for folder,pname,mode in [('hwr200-benchmark','hwr200-2-scans','literal'),('hwr200-expanded','hwr200-31-scans','literal')]:
 base=ROOT/'outputs'/folder;m=json.load(open(base/'manifest.json'));rr=[]
 if folder=='hwr200-expanded':
  for w in m['writers']:
   ss=[s for s in m['samples']if s['role']=='target'and s['writer']==w];ss.sort(key=lambda s:int(''.join(c for c in Path(s['local']).stem if c.isdigit())))
   files=[]
   for s in ss:
    p=base/s['local'];assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'];files.append(add(p))
   rr.append(rec(f'hwr-expanded-{w:03}',files,(base/f'evaluator/writer{w:03}.txt').read_text()))
 else:
  # These two full scans were manually scoped at their physical page boundaries.
  for w in [3,5]:
   p=base/f'targets/writer{w:03}-original{w}-page01.jpg';rr.append(rec(f'hwr-pilot-{w:03}',[add(p)],(base/f'evaluator/writer{w:03}.txt').read_text()))
 panel(pname,rr,mode,notes='Same frozen original scan bytes and evaluator scope as the existing comparison. Supplied source transcriptions, not independently verified word by word.')
(out/'inputs.json').write_text(json.dumps({'items':list(items.values()),'inference_receives_no_gold':True},indent=2));(out/'evaluator.json').write_text(json.dumps({'gold':gold,'panels':panels},ensure_ascii=False,indent=2));print('Prepared',len(items),'distinct input/scope tasks;',len(panels),'scoring panels')
