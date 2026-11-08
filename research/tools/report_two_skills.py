"""Score saved standalone-skill runs. No inference, network or retries."""
from pathlib import Path
import argparse,json,sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'handoffs/skill-reference-evaluation'))
from cer import score

def paired(rows,targets,gold,a,b,collection):
    by={(r['condition'],r['id']):r for r in rows}
    ids=[t['id'] for t in targets if t['collection']==collection and all(by.get((k,t['id']),{}).get('status')=='completed' for k in [a,b])]
    if not ids:return None
    result={'matched_targets':ids,'baseline':a,'comparison':b,'scores':{}}
    for condition in [a,b]:
        ss=[score(gold[i],by[condition,i]['transcription'],'reading') for i in ids]
        e=sum(x['edits'] for x in ss);n=sum(x['reference_characters'] for x in ss)
        result['scores'][condition]={'edits':e,'reference_characters':n,'cer':e/n}
    aa,bb=[result['scores'][k]['cer'] for k in [a,b]]
    result['relative_error_reduction']=None if aa==0 else (aa-bb)/aa
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args();base=args.run_dir
    gold=json.loads((base/'evaluator/gold.json').read_text());targets=json.loads((base/'targets/targets.json').read_text());runs={}
    for path in (base/'predictions').glob('*.json'):
        if not re.fullmatch(r'(?:sol|astra)-[A-G]\.json',path.name):continue
        model,condition=path.stem.split('-',1)
        rows=json.loads(path.read_text());runs.setdefault(model,[]).extend([{**r,'condition':condition} for r in rows])
    states={}
    for path in (base/'api').glob('*/predictions.json'):
        name=path.parent.name;runs[name]=json.loads(path.read_text());r=json.loads((path.parent/'run.json').read_text());states[name]={k:r.get(k) for k in ['model','status','cost_usd','new_budget_usd','scope']}
    output={'normalization':'NFC, case/punctuation ignored, whitespace collapsed; ё distinct from е. Placeholder letters such as unclear remain part of the scored output. No post-hoc exclusions. Letter targets are preselected resolved excerpts, not complete letters.','runs':{},'provider_states':states}
    for model,rows in runs.items():
        if len({(r['condition'],r['id']) for r in rows})!=len(rows):raise ValueError('Duplicate primary attempts: '+model)
        record={'attempts':len(rows),'statuses':[{'id':r['id'],'condition':r['condition'],'status':r['status']} for r in rows],'comparisons':{}}
        for coll in ['diary','letters']:
            record['comparisons'][coll]={}
            for name,a,b in [('reading_without_references','A','B'),('reading_with_raw_references','C','D'),('raw_extraction_instructions','E','D'),('verified_extraction_instructions','G','F')]:
                record['comparisons'][coll][name]=paired(rows,targets,gold,a,b,coll)
        output['runs'][model]=record
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n');print('Scored',len(runs),'saved run groups; matched target sets only; no model calls.')
if __name__=='__main__':main()
