"""Resume exact ZIP-member downloads, checking central-directory CRCs."""
import concurrent.futures
import hashlib
import json
import struct
import urllib.request
import zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'download-manifest.json').read_text())
def fetch(item):
    dest=Path(item['path'])
    if not dest.exists():
        offset=item['offset'];end=offset+30+len(item['name'].encode())+512+item['compressed']
        url=f'https://huggingface.co/datasets/AntiplagiatCompany/HWR200/resolve/{manifest["revision"]}/{item["archive"]}?member={offset}'
        req=urllib.request.Request(url,headers={'Range':f'bytes={offset}-{end}'})
        with urllib.request.urlopen(req,timeout=60) as response:
            assert response.status==206,'Refusing full archive download';data=response.read(end-offset+2)
        header=struct.unpack('<4s5H3I2H',data[:30]);assert header[0]==b'PK\x03\x04'
        start=30+header[-2]+header[-1];compressed=data[start:start+item['compressed']]
        raw=zlib.decompress(compressed,-15) if header[3]==8 else compressed
        assert header[3] in [0,8] and len(raw)==item['size'];assert zlib.crc32(raw)&0xffffffff==item['crc32']
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
    item['sha256']=hashlib.sha256(dest.read_bytes()).hexdigest();print(item['id'],'downloaded',flush=True)
    return item
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:manifest['sources']=list(pool.map(fetch,manifest['sources']))
(ROOT/'download-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
for writer in sorted({x['writer'] for x in manifest['sources']}):
    path=ROOT/f'groups/writer{writer:03}/sources.json';path.write_text(json.dumps(dict(writer=writer,pages=[x for x in manifest['sources'] if x['writer']==writer],status='downloaded_crc_and_hash_checked'),ensure_ascii=False,indent=2))
(ROOT/'sources-ready.json').write_text(json.dumps(dict(complete=True,pages=len(manifest['sources'])),indent=2))
print('AllsourceimagesdownloadedwithCRCchecks',flush=True)
