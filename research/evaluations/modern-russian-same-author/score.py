"""Whole-document CER; target labels stay evaluator-only."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
path=ROOT/'historical_metric.py'
if not path.exists():
    path=ROOT.parents[1]/'outputs/handwriting-reference-library/research/evaluations/open-system-selection/source/historical_metric.py'
spec=importlib.util.spec_from_file_location('metric',path)
metric=importlib.util.module_from_spec(spec);spec.loader.exec_module(metric)

def main():
    pages=json.loads((ROOT/'targets-only.json').read_text())['pages']
    reference=(ROOT/'evaluator/full-text.txt').read_text()
    rows=[]
    for model,condition in [(m,c) for m in ['astra','sol'] for c in 'ABC']+[('transkribus','plain')]:
        predictions=[];missing=[];hashes=[]
        for page in pages:
            f=ROOT/f'predictions/{model}/{condition}/{page["id"]}.json'
            if not f.exists():
                missing.append(page['id']);continue
            d=json.loads(f.read_text())
            assert d['input_sha256']==page['sha256'],f
            assert d['status']=='completed',f
            assert d['prediction'].strip(),f
            predictions.append(d['prediction'])
            hashes.append({'id':page['id'],'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
        row=dict(model=model,condition=condition,pages_completed=len(predictions),pages_expected=len(pages),missing=missing,prediction_hashes=hashes)
        if not missing:
            hypothesis='\n'.join(predictions)
            row.update({mode:metric.score(reference,hypothesis,mode) for mode in ['literal','reading']})
        rows.append(row)
    result=dict(writer=16,target_document='fpr16',source_document='original16',scoring_unit='entire nine-page document, numeric page order; no inferred per-page gold',
                reference_sha256=hashlib.sha256((ROOT/'evaluator/full-text.txt').read_bytes()).hexdigest(),
                normalization={'literal':'NFC and whitespace collapse; punctuation and case retained','reading':'NFC, casefold, Unicode punctuation removal, whitespace collapse; ё retained'},
                rows=rows,limits=['One writer, one run per condition; no estimate of model run variability.','Supplied full-text labels may differ from copied handwriting; results count label disagreement, not independently audited visual error.'])
    (ROOT/'metrics.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    with (ROOT/'metrics.csv').open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['model','condition','pages_completed','pages_expected','literal_edits','literal_characters','literal_CER_percent','reading_edits','reading_characters','reading_CER_percent'])
        for r in rows:
            w.writerow([r[k] for k in ['model','condition','pages_completed','pages_expected']]+[(100*r[m][k] if k=='cer' else r[m][k]) if m in r else '' for m in ['literal','reading'] for k in ['edits','characters','cer']])
    print(json.dumps([{k:v for k,v in r.items() if k not in ['prediction_hashes','missing']} for r in rows],ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
