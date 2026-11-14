"""Import unchanged TXT; require server-exported input bytes to match."""
import hashlib
import json
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parent
archive=ROOT/'transkribus-export-32002377.zip'
pages=json.loads((ROOT/'targets-only.json').read_text())['pages']
dest=ROOT/'predictions/transkribus/plain';dest.mkdir(parents=True,exist_ok=True)
archive_hash=hashlib.sha256(archive.read_bytes()).hexdigest()
verified=[]
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for page in pages:
        stem=f'{page["page"]:04d}_page{page["page"]:02d}'
        def member(suffix):
            names=[n for n in z.namelist() if Path(n).name==stem+suffix]
            assert len(names)==1,names
            return names[0]
        image_hash=hashlib.sha256(z.read(member('.jpg'))).hexdigest()
        assert image_hash==page['sha256']
        raw=z.read(member('.txt'));text=raw.decode('utf-8-sig')
        xml=ET.fromstring(z.read(member('.xml')))
        line_count=sum(e.tag.endswith('}TextLine') for e in xml.iter())
        record=dict(id=page['id'],input_sha256=page['sha256'],exported_image_sha256=image_hash,status='completed',
                    prediction=text,model_id=148545,recognition_job_id=32002332,export_job_id=32002377,
                    exported_TextLine_count=line_count,source_text_member=member('.txt'),
                    source_text_sha256=hashlib.sha256(raw).hexdigest(),export_zip_sha256=archive_hash,
                    no_skill=True,no_references=True,transport='UTF-8 with optional BOM removed; transcription unchanged')
        (dest/(page['id']+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2))
        verified.append(dict(id=page['id'],input_sha256=image_hash,exported_TextLine_count=line_count))
status=json.loads((ROOT/'transkribus-status.json').read_text())
status.update(status='completed_and_imported',export_zip_sha256=archive_hash,verified_images=verified,
              metadata_privacy='Original ZIP retained locally; public prediction records omit account metadata')
(ROOT/'transkribus-status.json').write_text(json.dumps(status,indent=2))
print('Verified and imported',len(verified),'unchanged page TXT files with byte-identical server-exported image hashes')
