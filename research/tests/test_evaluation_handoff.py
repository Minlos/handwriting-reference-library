"""Check blindness boundaries and scoring failures without a model or network."""
import unittest,sys,json,tempfile,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HANDOFF=ROOT/'handoffs/skill-reference-evaluation'
sys.path.insert(0,str(HANDOFF))
from prepare_inputs import render,packet
from cer import score

class EvaluationHandoffTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.protocol,cls.skill,cls.labels,cls.assets=render()
 def test_condition_files_do_not_leak_answers(self):
  for target in self.protocol['targets']:
   for c in 'ABCD':
    files=packet(target['page'],c,self.protocol,self.skill,self.labels,self.assets)
    self.assertEqual('SKILL.md' in files,c in 'BD')
    self.assertEqual('reference-labels.json' in files,c in 'CD')
    self.assertEqual(sum(n.startswith('reference-') and n.endswith('.jpg') for n in files),3 if c in 'CD' else 0)
    self.assertFalse(any('gold' in n or 'profile' in n or 'error-log' in n for n in files))
    self.assertEqual(len([n for n in files if n.startswith('target-')]),1)
 def test_failed_page_prevents_aggregate(self):
  rows=[]
  for t in self.protocol['targets']:
   rows.append(dict(setup='fixture',model='fixture',trial=1,condition='A',page=t['page'],status='completed',transcription=(HANDOFF/t['gold_file']).read_text()))
  rows[-1].update(status='error',transcription=None)
  with tempfile.TemporaryDirectory() as d:
   pred=Path(d)/'pred.jsonl';out=Path(d)/'score.json';pred.write_text(''.join(json.dumps(r)+'\n' for r in rows))
   subprocess.run([sys.executable,str(HANDOFF/'score_results.py'),'--predictions',str(pred),'--output',str(out)],check=True,capture_output=True)
   scored=json.loads(out.read_text());self.assertIsNone(scored['groups'][0]['conditions']['A']['aggregate']);self.assertEqual(scored['rows'][-1]['status'],'error')
 def test_cer_counts_insertions_deletions_and_substitutions(self):
  self.assertEqual(score('abcd','axcde')['edits'],2)
  self.assertEqual(score('abcd','acd')['edits'],1)
  self.assertEqual(score('Ёж!','еж','reading')['edits'],1)
  with self.assertRaises(ValueError):score('','x')

if __name__=='__main__':unittest.main()
