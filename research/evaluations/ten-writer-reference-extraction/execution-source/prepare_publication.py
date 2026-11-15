"""Stage public Apache-2.0 benchmark data only; never copy account/budget/credential files."""
from pathlib import Path
import json,hashlib,shutil,zipfile,sys
R=Path(__file__).resolve().parent;W=R.parents[1];D=W/'work/ten-writer-study-publication';D.mkdir(exist_ok=True)
H=lambda b:hashlib.sha256(b).hexdigest()
assert len([p for p in (R/'predictions').glob('*/*/rep*/writer*.json') if '-raw-' not in p.name])==174,'Refuse incomplete public bundle'
assert json.loads((R/'deepseek-summary.json').read_text())['attempted_documents']==60
folders=['sources','targets','packets','source-transcriptions','groups','predictions','deepseek-api','russian-crnn','reader-tasks','extractor-tasks']
files=[]
for folder in folders:
 files.extend(p for p in (R/folder).rglob('*') if p.is_file() and p.suffix.lower() in ['.jpg','.jpeg','.png','.json','.txt'])
files.extend(p for p in (R/'evaluator').rglob('*') if p.is_file() and 'audit-sheets' not in p.parts and p.suffix in ['.json','.txt'])
roots=['manifest.json','download-manifest.json','inputs.json','input-validation.json','final-input-verification.json','packet-validation.json','prediction-validation.json','baseline-settings.json','metrics.json','metric-verification.json','deepseek-summary.json','deepseek-failures.json','api-raw-preservation.json','public-runtime-verification.json']
files.extend(R/x for x in roots if (R/x).exists());files=sorted(set(files))
for p in files:
 assert p.is_relative_to(R) and p.name not in ['budget.json','replay-budget.json']
 if p.suffix in ['.json','.txt']:
  t=p.read_text();assert not any(x in t for x in ['Bearer sk-','DEEPSEEK_API_KEY=sk-','Authorization: Bearer'])
archive=D/'hwr200-ten-writer-reference-data-2026-11-15.zip';manifest=[]
licensefile=W/'outputs/handwriting-reference-library/research/evaluations/open-system-selection/LICENSE-HWR200-APACHE-2.0.txt'
with zipfile.ZipFile(archive,'w',allowZip64=True) as z:
 for p in files:
  name=str(p.relative_to(R));b=p.read_bytes();z.writestr(name,b,compress_type=zipfile.ZIP_STORED if p.suffix.lower() in ['.jpg','.jpeg','.png'] else zipfile.ZIP_DEFLATED);manifest.append(dict(path=name,bytes=len(b),sha256=H(b)))
 z.writestr('LICENSE-HWR200-APACHE-2.0.txt',licensefile.read_bytes(),compress_type=zipfile.ZIP_DEFLATED)
 z.writestr('data-file-manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',compress_type=zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert not any(Path(x).name=='README.md' or x.endswith(('.py','.md','.sh')) for x in z.namelist())
 for row in manifest:assert H(z.read(row['path']))==row['sha256']
record=dict(filename=archive.name,bytes=archive.stat().st_size,sha256=H(archive.read_bytes()),data_files=len(manifest),integrity='All ZIP CRCs and every entry SHA-256 verified',contains='Public HWR200 native sources/targets, crop audit data, frozen reader inputs/outputs, evaluator labels and metrics; no skill, README, scripts, credentials or shared account files',dataset_license='Apache-2.0',source='AntiplagiatCompany/HWR200',revision='366a882a2b8d043d437126d2878bd3812ec55a94')
(D/'data-archive.json').write_text(json.dumps(record,indent=2)+'\n')
for p in (R/'public-runtime').glob('*.py'):shutil.copy2(p,D/p.name)
for name in ['score.py','historical_metric.py','verify_metrics.py','validate_predictions.py','preserve_api_raw.py']:
 shutil.copy2(R/name,D/name)
for name in ['protocol.public.json','reader-prompt.txt','replay-budget.example.json']:shutil.copy2(R/'public-runtime'/name,D/name)
for name in ['metrics.json','baseline-settings.json','deepseek-summary.json','deepseek-failures.json','metric-verification.json','public-runtime-verification.json']:shutil.copy2(R/name,D/name)
shutil.copytree(R/'skill-snapshots',D/'skill-snapshots',dirs_exist_ok=True)
shutil.copy2(R/'reference-packet-review.html',D/'reference-packet-review.html');shutil.copy2(licensefile,D/licensefile.name)
print(json.dumps(record,indent=2))
