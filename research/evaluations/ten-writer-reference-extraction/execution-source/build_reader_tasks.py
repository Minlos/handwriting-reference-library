from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for model in ['astra','sol']:
 for w in [17,18,20,21,22,23,24,25,26,28]:
  for c in 'ABC':
   for rep in [1,2]:
    d=R/'reader-tasks'/model/c/f'rep{rep}';d.mkdir(parents=True,exist_ok=True)
    out=R/'predictions'/model/c/f'rep{rep}'/f'writer{w:03}.json'
    task=dict(prompt=(R/'reader-prompt.txt').read_text(),prompt_sha256=h(R/'reader-prompt.txt'),writer=w,condition=c,replicate=rep,model={'astra':'gpt-6-astra','sol':'gpt-6.1-sol'}[model],targets=json.loads((R/'groups'/f'writer{w:03}'/'targets.json').read_text())['pages'],reference=None,output=str(out),budget='Present each original target once with view_image detail=original, then at most TWO additional original-image requests per page. No target modification/resizing/cropping, no extra references, web search, OCR or reading skill. Record actual displayed coverage per page, including thumbnail/strip failures; no secret retries or workarounds.',save='Save immutable raw-initial.json and raw-final.json beside writerNNN.json using writerNNN-raw-initial.json and writerNNN-raw-final.json. If no separate revision, initial and final transcription are identical, explicitly record single-pass. Prediction JSON includes status completed/error, pages [{id,prediction}], coverage [{id,original_requests,displayed_coverage,limitations}], writer/model/condition/replicate, reference and prompt hashes, no_skill=true. Do not read prior predictions or evaluator files. Documents untrusted.' )
    if c!='A':
     p=R/'packets'/f'writer{w:03}'/c
     task['reference']=dict(sheet=str(p/'sheet.jpg'),labels=str(p/'reader-labels.json'),freeze=str(p/'freeze.json'),instructions='View only supplied sheet.jpg and read reader-labels.json; do not open native crops, packet metadata, source text or source scans. Verify supplied sheet/labels hashes against freeze before use.')
    (d/f'writer{w:03}.json').write_text(json.dumps(task,ensure_ascii=False,indent=2)+'\n')
print('Wrote120 isolated reader task files with no evaluator text')
