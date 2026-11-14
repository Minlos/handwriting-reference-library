"""Fetch selected original ZIP members from a pinned public dataset revision."""
import concurrent.futures
import hashlib
import json
import struct
import urllib.request
import zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'download-manifest.json').read_text())
base=f'https://huggingface.co/datasets/AntiplagiatCompany/HWR200/resolve/{manifest["revision"]}/{manifest["archive"]}'

def fetch(item):
    dest=ROOT/item['local']
    if not dest.exists():
        start=item['offset'];end=start+30+len(item['name'].encode())+100+item['compressed']
        request=urllib.request.Request(base+f'?member={start}',headers={'Range':f'bytes={start}-{end}'})
        with urllib.request.urlopen(request,timeout=40) as r:
            if r.status!=206:
                raise RuntimeError('Refusing full archive download')
            data=r.read(end-start+2)
        header=struct.unpack('<4s5H3I2H',data[:30])
        assert header[0]==b'PK\x03\x04' and header[3]==8
        offset=30+header[-2]+header[-1]
        image=zlib.decompress(data[offset:offset+item['compressed']],-15)
        assert len(image)==item['size']
        assert zlib.crc32(image)&0xffffffff==header[6]
        dest.parent.mkdir(exist_ok=True,parents=True);dest.write_bytes(image)
    item['sha256']=hashlib.sha256(dest.read_bytes()).hexdigest()
    print(item['role'],item['local'],dest.stat().st_size,flush=True)
    return item

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    manifest['entries']=list(pool.map(fetch,manifest['entries']))
(ROOT/'download-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
