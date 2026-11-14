from pathlib import Path
import json,zipfile,hashlib,re
R=Path(__file__).resolve().parent;arc=R/'transkribus-export-job-32001301.zip';out=R/'transkribus';out.mkdir(exist_ok=True);items=json.loads((R/'inputs.json').read_text())['items'];verified=[]
with zipfile.ZipFile(arc)as z:
 assert z.testzip()is None
 for s in items:
  candidates=[n for n in z.namelist()if '/txt/'in n and Path(n).name.endswith(s['id']+'.txt')];assert len(candidates)==1,candidates;name=candidates[0];raw=z.read(name);hyp=raw.decode('utf-8-sig')
  ims=[n for n in z.namelist()if Path(n).suffix.lower()in ['.jpg','.jpeg','.png'] and re.search(r'_'+s['id']+r'\.',Path(n).name)];assert len(ims)==1,ims;image_raw=z.read(ims[0]);digest=hashlib.sha256(image_raw).hexdigest();assert digest==s['sha256'],(s['id'],digest,s['sha256'])
  record={'id':s['id'],'input_sha256':s['sha256'],'exported_image_sha256':digest,'status':'completed','prediction':hyp,'engine':'Transkribus Russian generic handwritten and typed1','model_id':148545,'recognition_job_id':32001209,'export_job_id':32001301,'source_text_member':name,'source_text_sha256':hashlib.sha256(raw).hexdigest(),'text_transport_decoding':'UTF-8 with optional BOM removed; no transcription edits','export_zip_sha256':hashlib.sha256(arc.read_bytes()).hexdigest(),'no_skill':True,'no_references':True}
  (out/(s['id']+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2));verified.append(s['id'])
(out/'settings.json').write_text(json.dumps({'model_id':148545,'model_name':'Russian generic handwritten and typed1','pages':9,'credits_used':9,'duration_seconds':390.473,'input_images_exported_byte_identically':verified,'raw_archive':arc.name,'segmentation':'Transkribus quick-recognition defaults; automatic page segmentation','metadata_privacy':'Original export retained locally. Public predictions omit account metadata; exported TXT content is unchanged.'},indent=2))
p=R/'score.py';s=p.read_text().replace("'apple-vision','rehand'","'apple-vision','transkribus','rehand'");p.write_text(s)
print('PASS:9 unedited page transcripts imported; all9 server-exported original-image hashes match the shared input bytes')
