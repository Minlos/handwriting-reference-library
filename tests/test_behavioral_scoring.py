import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('behavior',Path(__file__).resolve().parents[1]/'tools/score_behavioral_cases.py')
m = importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class BehavioralScoring(unittest.TestCase):
    def test_plausible_substitution_is_an_error(self):
        c={'id':'B01','kind':'image_reading','expected_text':'хочила'}
        r=m.score_case(c,{'text':'хотела','visually_checked':True})
        self.assertEqual(r['errors'],2)
        self.assertFalse(r['passed'])

    def test_correction_is_not_visual_evidence(self):
        c={'id':'B05','kind':'correction_handling','expected_text':'настроение ничего','expected_visual_claim':False}
        self.assertFalse(m.score_case(c,{'text':'настроение ничего','visually_checked':True})['passed'])
        self.assertTrue(m.score_case(c,{'text':'настроение ничего','visually_checked':False})['passed'])

    def test_not_run_is_not_a_perfect_score(self):
        r=m.score_case({'id':'B07'},None)
        self.assertEqual(r['status'],'not_run')
        self.assertNotIn('passed',r)

if __name__ == '__main__':unittest.main()
