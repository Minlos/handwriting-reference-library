from pathlib import Path
import json,hashlib,shutil
root=Path.cwd();src=root/'outputs/public-handwriting-corpus/hwr200';out=root/'work/open-system-selection';docs=json.loads((src/'documents.json').read_text());pages=[];gold={}
for d in docs:
 if not d['complete'] or len(d['images'])!=1:continue
 ident=f'writer{d["writer"]:03}';p=src/d['images'][0];dest=out/'inputs'/(ident+p.suffix.lower());shutil.copy2(p,dest)
 pages.append({'id':ident,'path':str(dest),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'writer':d['writer'],'document':d['document'],'source_path':d['images'][0],'scope':'all','line':False});gold[ident]=(src/d['text']).read_text()
assert len(pages)==9
(out/'inputs.json').write_text(json.dumps({'items':pages,'inference_receives_no_gold':True},indent=2))
(out/'evaluator/gold.json').write_text(json.dumps(gold,ensure_ascii=False,indent=2))
(out/'protocol.json').write_text(json.dumps({'status':'running','sample':'All nine complete single-scan documents in the downloaded pinned HWR200 subset; selected by metadata, not recognition performance.','revision':'366a882a2b8d043d437126d2878bd3812ec55a94','source':'https://huggingface.co/datasets/AntiplagiatCompany/HWR200','pages':9,'writers':9,'text_ids':len(set(p['document']for p in pages)),'labels':'Upstream supplied full-document texts; not independently verified. Audit scan/reference correspondence before ranking.','normalization':{'literal':'NFC whitespace collapse; case and punctuation retained','reading':'NFC casefold Unicode punctuation removal whitespace collapse; ё retained'},'input_rule':'Identical original source bytes for all systems. No references or skill supplied to either general LLM in this baseline comparison.','candidates':['Sol','Astra','Rehand','Tesseract','EasyOCR','Kraken-small','Russian-CRNN','PaddleOCR','Calamari'],'limitations':['Nine writers but eight distinct source texts; original2 is repeated across two writers.','Selection benchmark only; future confirmation uses different material.']},indent=2))
print('Prepared',len(pages),'public pages;',len(set(p['document']for p in pages)),'distinct source texts')
