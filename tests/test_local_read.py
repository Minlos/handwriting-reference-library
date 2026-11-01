import base64,hashlib,json,tempfile,unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from local_read import RunConfig,run_pipeline,validate_local_url
from PIL import Image

class FakeOllama:
 def __init__(self,truncate=False,cloud=False):self.calls=[];self.gemma_calls=0;self.truncate=truncate;self.cloud=cloud
 def request(self,path,payload=None):
  self.calls.append((path,payload))
  if path=='/api/tags':return {'models':[{'name':'glm-ocr:latest','size':123},{'name':'gemma4:12b','size':123}]}
  if path=='/api/show':return {'capabilities':['vision','completion','thinking'],**({'remote_host':'https://ollama.com'} if self.cloud else {})}
  if payload['model']=='glm-ocr:latest':return {'done':True,'done_reason':'stop','response':'OCR text'}
  self.gemma_calls+=1
  reading='Independent reading' if self.gemma_calls==1 else 'Reviewed reading'
  result={'reading':reading,'uncertain_spans':['uncertain word'],'evidence':['Visible strokes'],'reference_ids_used':[]}
  return {'done':True,'done_reason':'length' if self.truncate else 'stop','response':json.dumps(result)}

class LocalWorkflowTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.image=self.root/'input.png';Image.new('RGB',(40,30),'white').save(self.image)
 def tearDown(self):self.temp.cleanup()
 def config(self,**kw):return RunConfig(image=self.image,output_dir=self.root/'run',**kw)
 def reference(self,category='verified',tamper=False):
  lib=self.root/'library';lib.mkdir();p=lib/'reference.png';Image.new('RGB',(30,20),'black').save(p)
  digest=hashlib.sha256(p.read_bytes()).hexdigest();entry={'id':'V1','label':'Reference label','category':category,'crop_path':'reference.png','crop_sha256':'bad' if tamper else digest}
  (lib/'index.json').write_text(json.dumps({'entries':[entry]}));return lib
 def test_local_endpoint_only(self):
  for url in ['https://example.com','http://127.0.0.1@evil.test','http://localhost:123/api/generate','http://localhost:123/?x=1']:
   with self.assertRaises(ValueError):validate_local_url(url)
  self.assertEqual(validate_local_url('http://127.0.0.1:11434/'),'http://127.0.0.1:11434')
 def test_three_stages_keep_images_and_labels_unchanged(self):
  lib=self.reference();before=(lib/'index.json').read_bytes();fake=FakeOllama();result=run_pipeline(self.config(library=lib,references=('V1',)),fake)
  calls=[p for path,p in fake.calls if path=='/api/generate'];self.assertEqual(len(calls),3)
  self.assertNotIn('OCR text',calls[0]['prompt']);self.assertNotIn('Independent reading',calls[1]['prompt'])
  self.assertEqual(calls[1]['prompt'],'Text Recognition:');self.assertNotIn('system',calls[1])
  self.assertEqual(len(calls[1]['images']),1)
  self.assertIn('OCR text',calls[2]['prompt']);self.assertIn('Independent reading',calls[2]['prompt'])
  for payload in calls:
   self.assertEqual(hashlib.sha256(base64.b64decode(payload['images'][0])).hexdigest(),result['target']['prepared_sha256'])
  self.assertEqual((lib/'index.json').read_bytes(),before);self.assertEqual(result['status'],'review_required');self.assertFalse(result['verified_labels_modified'])
 def test_dry_run_never_calls_models(self):
  fake=FakeOllama();result=run_pipeline(self.config(dry_run=True),fake);self.assertFalse(fake.calls);self.assertEqual(result['status'],'dry_run')
 def test_no_overwrite_or_api_call_on_existing_output(self):
  output=self.root/'run';output.mkdir();(output/'keep').write_text('keep');fake=FakeOllama()
  with self.assertRaises(FileExistsError):run_pipeline(self.config(),fake)
  self.assertFalse(fake.calls);self.assertEqual((output/'keep').read_text(),'keep')
 def test_bad_reference_hash_is_rejected_before_requests(self):
  fake=FakeOllama();lib=self.reference(tamper=True)
  with self.assertRaises(ValueError):run_pipeline(self.config(library=lib,references=('V1',)),fake)
  self.assertFalse(fake.calls)
 def test_provisional_reference_requires_explicit_opt_in(self):
  lib=self.reference(category='provisional')
  with self.assertRaises(ValueError):run_pipeline(self.config(library=lib,references=('V1',)),FakeOllama())
  result=run_pipeline(self.config(library=lib,references=('V1',),allow_provisional=True),FakeOllama());self.assertEqual(result['references'][0]['category'],'provisional')
 def test_cloud_alias_is_rejected_before_image_requests(self):
  fake=FakeOllama(cloud=True)
  with self.assertRaises(ValueError):run_pipeline(self.config(),fake)
  self.assertFalse(any(p=='/api/generate' for p,_ in fake.calls))
 def test_identical_target_cannot_be_a_labeled_reference(self):
  lib=self.reference();Image.open(lib/'reference.png').save(self.image)
  with self.assertRaises(ValueError):run_pipeline(self.config(library=lib,references=('V1',)),FakeOllama())
 def test_raw_coordinates_and_rotation_reproduce_pixels(self):
  im=Image.new('RGB',(10,8));im.putpixel((3,2),(255,0,0));im.save(self.image)
  result=run_pipeline(self.config(box=(2,1,7,6),rotation=90,dry_run=True),FakeOllama())
  with Image.open(self.root/'run/target.png') as actual:self.assertEqual(actual.tobytes(),im.crop((2,1,7,6)).rotate(90,expand=True).tobytes())
  self.assertEqual(result['target']['original_box'],(2,1,7,6));self.assertEqual(result['target']['rotation_ccw'],90)
 def test_truncated_review_cannot_become_proposed_reading(self):
  result=run_pipeline(self.config(),FakeOllama(truncate=True));self.assertIsNone(result['stages']['gemma_review']['reading']);self.assertEqual(result['stages']['gemma_review']['status'],'incomplete');self.assertEqual(result['status'],'review_required')

if __name__=='__main__':unittest.main()
