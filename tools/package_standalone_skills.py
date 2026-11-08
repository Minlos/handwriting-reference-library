"""Build portable skill ZIPs, keeping optional test inputs below test-material/."""
from pathlib import Path
import hashlib,json,zipfile

ROOT=Path(__file__).resolve().parents[1]

def build(name):
    folder=ROOT/'skills'/name
    target=ROOT/'downloads'/(name+'.zip')
    members={str(p.relative_to(folder)):p for p in folder.rglob('*') if p.is_file()}
    manifest=json.loads((folder/'test-material/inputs.json').read_text())
    for entry in manifest:
        source=ROOT/entry['repository_path']
        assert source.is_file(),source
        members['test-material/'+entry['packet_path']]=source
    hashes={key:hashlib.sha256(p.read_bytes()).hexdigest() for key,p in members.items()}
    target.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
        for key,path in sorted(members.items()):archive.write(path,name+'/'+key)
        archive.writestr(name+'/test-material/file-hashes.json',json.dumps(hashes,indent=2)+'\n')
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        for key,digest in hashes.items():assert hashlib.sha256(archive.read(name+'/'+key)).hexdigest()==digest
        assert name+'/SKILL.md' in archive.namelist()
    return {'skill':name,'zip':str(target.relative_to(ROOT)),'bytes':target.stat().st_size,'input_images':len(manifest),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}

if __name__=='__main__':
    for skill in ['extract-handwriting-references','read-handwriting']:print(json.dumps(build(skill)))
