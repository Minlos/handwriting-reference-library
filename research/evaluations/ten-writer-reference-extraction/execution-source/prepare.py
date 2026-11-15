"""Select independent writer-document pairs before any recognition results."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[1]
DATA=WORKSPACE/'outputs/public-handwriting-corpus/hwr200'
WRITERS=[17,18,20,21,22,23,24,25,26,28]
docs=json.loads((DATA/'documents.json').read_text())
index=[x for f in (DATA/'indexes').glob('*.json') for x in json.loads(f.read_text())]
source_downloads=[];groups=[]
with zipfile.ZipFile(DATA/'annotations.zip') as labels:
    for writer in WRITERS:
        doc=next(x for x in docs if x['writer']==writer);assert doc['complete']
        targets=[]
        for number,name in enumerate(doc['images'],1):
            source=DATA/name;dest=ROOT/f'targets/writer{writer:03}'/f'page{number:02}{source.suffix.lower()}'
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
            targets.append(dict(id=f'writer{writer:03}-target-{number:02}',writer=writer,page=number,path=str(dest.resolve()),sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
        entries=sorted([x for x in index if x['name'].startswith(f'hw_dataset/{writer}/fpr{writer}/Сканы/') and Path(x['name']).suffix.lower() in ['.jpg','.jpeg','.png']],key=lambda x:int(Path(x['name']).stem))
        assert entries
        sources=[]
        for number,item in enumerate(entries,1):
            dest=ROOT/f'sources/writer{writer:03}'/f'page{number:02}{Path(item["name"]).suffix.lower()}'
            row=dict(item,id=f'writer{writer:03}-source-{number:02}',writer=writer,page=number,path=str(dest.resolve()))
            sources.append(row);source_downloads.append(row)
        for role,member in [('source',f'annotations/FPR/{writer}/fpr{writer}.json'),('target',f'annotations/Originals/{writer}/original{writer}.json')]:
            data=json.loads(labels.read(member));out=ROOT/('source-transcriptions' if role=='source' else 'evaluator/published')/f'writer{writer:03}.txt'
            out.parent.mkdir(parents=True,exist_ok=True);out.write_text(data['full_text'])
        group=ROOT/f'groups/writer{writer:03}';group.mkdir(parents=True,exist_ok=True)
        (group/'targets.json').write_text(json.dumps(dict(writer=writer,pages=targets),indent=2))
        (group/'sources.json').write_text(json.dumps(dict(writer=writer,pages=sources,status='download_pending'),indent=2))
        groups.append(dict(writer=writer,source_document=f'fpr{writer}',target_document=f'original{writer}',source_pages=len(sources),target_pages=len(targets)))
(ROOT/'download-manifest.json').write_text(json.dumps(dict(revision='366a882a2b8d043d437126d2878bd3812ec55a94',sources=source_downloads),ensure_ascii=False,indent=2))
(ROOT/'manifest.json').write_text(json.dumps(dict(dataset='AntiplagiatCompany/HWR200',writers=WRITERS,groups=groups,source_pages=sum(x['source_pages'] for x in groups),target_pages=sum(x['target_pages'] for x in groups),selection='Ten distinct modern writers and distinct target text families, excluding prior development/validation writer IDs. Source FPR document and separate full original target document per writer. Fixed before recognition.',label_status='Published source text; audit required before recognition, not human-verified'),indent=2))
freeze=ROOT/'skill-snapshots';freeze.mkdir(exist_ok=True)
repo=WORKSPACE/'outputs/handwriting-reference-library'
shutil.copy2(repo/'skills/extract-handwriting-references/SKILL.md',freeze/'extract-handwriting-references.md')
shutil.copy2(repo/'skills/read-handwriting/SKILL.md',freeze/'read-handwriting-current.md')
shutil.copy2(WORKSPACE/'work/read-handwriting-development/candidate/SKILL.md',freeze/'read-handwriting-candidate.md')
(ROOT/'status.json').write_text(json.dumps(dict(phase='source_download_and_label_audit',writers=10,source_pages=sum(x['source_pages'] for x in groups),target_pages=sum(x['target_pages'] for x in groups),recognition_started=False),indent=2))
print('Selected10writers;',sum(x['source_pages'] for x in groups),'source scans;',sum(x['target_pages'] for x in groups),'held-out scans')
