"""Score selected development pages; exclude the selection-visible pilot."""
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
    pages=json.loads((ROOT/'reader-inputs.json').read_text())
    gold_path=ROOT/'evaluator/gold.json'
    if not gold_path.exists():
        gold_path=ROOT.parent/'open-system-selection/evaluator/gold.json'
    gold=json.loads(gold_path.read_text())
    results=[]
    for variant in ['P0','PV','PVC','PVR','PVCR','PFULL']:
        rows=[]
        for page in pages:
            f=ROOT/f'predictions/{variant}/{page["id"]}.json'
            if not f.exists():continue
            d=json.loads(f.read_text())
            if d.get('status')!='completed':continue
            assert d['input_sha256']==page['sha256']
            rows.append(dict(id=page['id'],actual_view_count=d['actual_view_count'],
                             initial={m:metric.score(gold[page['id']],d['initial_prediction'],m) for m in ['literal','reading']},
                             final={m:metric.score(gold[page['id']],d['prediction'],m) for m in ['literal','reading']}))
        r=dict(variant=variant,completed=len(rows),expected=len(pages),pages=rows)
        if len(rows)==len(pages):
            r['aggregate']={}
            for stage in ['initial','final']:
                r['aggregate'][stage]={}
                for mode in ['literal','reading']:
                    edits=sum(x[stage][mode]['edits'] for x in rows);chars=sum(x[stage][mode]['characters'] for x in rows)
                    r['aggregate'][stage][mode]=dict(edits=edits,characters=chars,cer=edits/chars)
        results.append(r)
    baseline=[]
    for page in pages:
        f=ROOT/f'baseline/transkribus/{page["id"]}.json'
        if not f.exists():continue
        b=json.loads(f.read_text());assert b['input_sha256']==page['sha256']
        baseline.append({m:metric.score(gold[page['id']],b['prediction'],m) for m in ['literal','reading']})
    conventional=dict(engine='Transkribus 148545, default automatic layout',completed=len(baseline),expected=len(pages),provenance='Reused unchanged outputs from the nine-page comparison for these identical image hashes and supplied labels; no new call.')
    if len(baseline)==len(pages):
        conventional['aggregate']={}
        for mode in ['literal','reading']:
            edits=sum(x[mode]['edits'] for x in baseline);chars=sum(x[mode]['characters'] for x in baseline)
            conventional['aggregate'][mode]=dict(edits=edits,characters=chars,cer=edits/chars)
    d=dict(results=results,conventional_baseline=conventional,limits=['Three retrospectively selected development pages, not an independent validation sample.','One run per condition, no separation of run variation from instruction effects.','Actual image inspections differ within a common maximum of three; extra effort is not controlled.','Supplied source texts contain known visual discrepancies, including writer035 темней versus label полней.','No source references supplied; this tests the reading skill separately from reference extraction.'])
    (ROOT/'metrics.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
    for r in results:
        print(r['variant'],str(r['completed'])+'/3',r.get('aggregate',{}))

if __name__=='__main__':main()
