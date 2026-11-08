from pathlib import Path
import importlib.util,json,unittest,hashlib
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('two_skills',ROOT/'research/tools/report_two_skills.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class TwoSkillReporting(unittest.TestCase):
 def test_failed_condition_keeps_matching_population(self):
  targets=[{'id':'x','collection':'letters'},{'id':'y','collection':'letters'}]
  rows=[{'id':'x','condition':'A','status':'completed','transcription':'bad'}, {'id':'x','condition':'B','status':'error','transcription':''}, {'id':'y','condition':'A','status':'completed','transcription':'аб'}, {'id':'y','condition':'B','status':'completed','transcription':'ав'}]
  result=module.paired(rows,targets,{'x':'long reference','y':'аб'},'A','B','letters')
  self.assertEqual(result['matched_targets'],['y']);self.assertEqual(result['scores']['A']['reference_characters'],2);self.assertEqual(result['scores']['B']['edits'],1)
 def test_unrun_has_no_score(self):self.assertIsNone(module.paired([],[],{},'A','B','letters'))
 def test_popov_sources_exclude_targets(self):
  rows=json.loads((ROOT/'skills/extract-handwriting-references/test-material/popov/raw-sources.json').read_text())
  self.assertEqual(len(rows),27);self.assertEqual(len({x['letter'] for x in rows}),14);self.assertFalse({'L01','L09','L13'} & {x['letter'] for x in rows})
 def test_actual_pixels_match_hashes_and_bounds(self):
  from PIL import Image
  folder=ROOT/'skills/read-handwriting/test-material/popov'
  for row in json.loads((folder/'targets.json').read_text()):
   p=folder/'input'/row['image'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),row['sha256']);x0,y0,x1,y1=row['bbox_xyxy']
   with Image.open(p) as im:self.assertEqual(im.size,(x1-x0,y1-y0))
if __name__=='__main__':unittest.main()
