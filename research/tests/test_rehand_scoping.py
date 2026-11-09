from pathlib import Path
import importlib.util,unittest
spec=importlib.util.spec_from_file_location('rehand',Path(__file__).resolve().parents[1]/'tools/score_rehand_popov.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class RehandScoping(unittest.TestCase):
 def test_scale_centers_not_intersections_and_keep_provider_order(self):
  boxes=[{'x':15,'y':20,'w':10,'h':10,'text':'second'}, {'x':2,'y':20,'w':10,'h':10,'text':'first'}, {'x':0,'y':0,'w':10,'h':10,'text':'outside'}]
  got=m.select_boxes(boxes,[0,40,60,60],(2,2))
  self.assertEqual([i for i,_ in got],[0,1])
 def test_exclusive_bottom_and_right_boundaries(self):
  b={'x':0,'y':0,'w':10,'h':10,'text':'edge'}
  self.assertEqual(m.select_boxes([b],[0,0,5,5],(1,1)),[])
if __name__=='__main__':unittest.main()
