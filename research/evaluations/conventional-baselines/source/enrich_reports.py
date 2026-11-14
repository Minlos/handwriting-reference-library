from pathlib import Path
import json,shutil,os,hashlib
ROOT=Path.cwd();repo=ROOT/'outputs/handwriting-reference-library';base=ROOT/'work/conventional-baselines';out=repo/'research/evaluations/conventional-baselines';out.mkdir(exist_ok=True)
metrics=json.load(open(base/'metrics.json'));results=metrics['results']
for name in ['metrics.json','evaluator.json','matched-populations.json','printed-control.json','tesseract-config-diagnostic.json']:shutil.copy2(base/name,out/name)
cat=json.load(open(base/'inputs.json'))
for r in cat['items']:r['path']=str(Path(r['path']).relative_to(ROOT))
(out/'inputs.json').write_text(json.dumps(cat,indent=2))
for eng in results:
 shutil.copytree(base/eng/'records',out/'raw'/eng,dirs_exist_ok=True);shutil.copy2(base/eng/'settings.json',out/'raw'/eng/'settings.json')
def frac(engine,panel,mode='reading',units=None):
 p=results[engine]['panels'][panel];rr=p['rows']
 if units is not None:rr=[r for r in rr if r['unit']in units]
 e=sum(r[mode]['edits']for r in rr);n=sum(r[mode]['characters']for r in rr);return f'{100*e/n:.2f}% ({e}/{n})'
def table(panels):
 s='| Evaluated material | Tesseract 5.5.4, Russian best | EasyOCR 1.7.2, Cyrillic |\n|---|---:|---:|\n'
 for label,panel,units,mode in panels:s+=f'| {label} | {frac("tesseract",panel,mode,units)} | {frac("easyocr",panel,mode,units)} |\n'
 return s
allpanels=[('14 selected diary crops','diary-14-crops',None,'reading'),('Diary pages 4, 6, 7','diary-3-pages',None,'reading'),('Diary pages 1, 2, 3, 5, 8, 9','diary-6-pages',None,'reading'),('Standalone reading/extraction: diary','two-skills-diary',None,'reading'),('Three Popov excerpts','two-skills-letters',None,'reading'),('HWR200 first pilot: 2 scans','hwr200-2-scans',None,'literal'),('HWR200 expanded: 31 scans / 10 documents','hwr200-31-scans',None,'literal')]
readme='''# Conventional OCR on the historical comparison sets

These tests add conventional OCR baselines to the existing handwriting comparisons. Each engine received the same frozen source image bytes as its corresponding test panel. Neither engine received reference transcriptions, author examples, skill instructions or another recognizer’s output. The collection downloads are separate from these evaluations.

Tesseract and EasyOCR completed all 59 distinct input/scope tasks without recognition-call errors. The seven scoring panels reuse overlapping inputs; they must not be added together or pooled into one accuracy figure. Empty OCR output is scored as omissions, not dropped. Fractions below are character edits / normalized reference characters. Lower CER is better.

'''+table(allpanels)+'''
The diary and letter rows use reading CER: NFC, casefold, Unicode punctuation removed, whitespace collapsed, ё retained. The HWR200 rows use literal CER: NFC and whitespace collapse, with case and punctuation retained, matching their principal reports. Both modes and per-target results are in metrics.json.

These two general OCR configurations perform poorly on this handwriting. That does not establish that conventional handwriting recognition is generally worse than LLMs. The existing six-page tests include Russian CRNN at 26.05% CER and Kraken-small at 31.13%; the selected 14-crop tests include CRNN at 17.11% and Kraken-small at 32.46%. Those configurations and populations remain separate. Rehand’s letter result used full-page images rather than the cropped LLM inputs, as its report explains.

## The baselines preserve each report’s scope

The matched three-page target PNGs cover pages 4, 6 and 7. Only the final unresolved word on page 6 is excluded. Its ink lies in rectangle [1560,2540,2150,2765] of the 2343×2765 frozen image. Detection centers inside that region are omitted from scoring; all raw detections are retained. EasyOCR’s one excluded detection and Tesseract’s zero excluded detections are recorded. No known neighboring text is excluded.

The Popov L09 fixture requests only the bottom complete line and contains partial neighboring ink. A fixed geometric adapter keeps the lowest detected line, grouping detections within half the maximum detected text height. The adapter uses coordinates, not evaluator answers. Full raw output remains available. The letter scores concern three short excerpts, not complete letters.

The standalone-skill report contains different completed target subsets for some models/conditions. matched-populations.json gives conventional scores for every one of those exact historical subsets. Compare those entries, not the full-panel aggregate, with a partial LLM row. The original two-skill denominators were checked against each rescore.

The historical contextual-assistant and Gemini/Vinnik inputs cannot be fully reconstructed as isolated calls. Their new baselines use the same evaluated page-6 region and reference; they are a same-text-scope comparison, not proof of identical original model inputs or effort.

## Configuration and evidence

Tesseract uses the official tessdata_best Russian LSTM, OEM 1, page segmentation mode 3 for pages/excerpts and mode 7 for supplied single-line crops. EasyOCR uses its Cyrillic generation-2 recognizer with Russian/English, the default CRAFT detector for pages/excerpts, greedy decoding, CPU, two Torch threads and a 2560-pixel detector canvas. Supplied single-line crops go directly to its recognizer. Settings and weight hashes are recorded under raw/. No language-model correction or target-specific parameter tuning was applied.

A separate synthetic printed-Russian control was read exactly by both engines. It is explicitly labeled synthetic and is not a corpus crop or an accuracy sample. An initial Tesseract wrapper configuration lacked its TSV output config in the custom model directory. That invalid attempt was excluded and all inputs were rerun with explicit tessedit_create_tsv=1. The diagnostic is retained; those setup errors were not reported as OCR accuracy.

Frozen evaluator labels preserve the historical comparisons. They include contributor-corrected working copies, hand-selected snippets and upstream supplied transcriptions; they are not all independently double-verified ground truth. Exact source images are indexed by SHA256. Runtime is recorded per input, excluding model download/setup, and there were no paid inference API calls.

Files: metrics.json contains raw per-panel predictions and literal/reading counts; evaluator.json contains the frozen scoring texts; inputs.json contains image paths, hashes and scope; raw/ contains complete outputs and settings; matched-populations.json contains subset-matched scores. Inference is kept separate from evaluator text.

Other applicable conventional software includes [PaddleOCR’s Cyrillic PP-OCR models](https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/version3.x/pipeline_usage/OCR.en.md) and [Calamari](https://github.com/Calamari-OCR/calamari). These two were not newly run here. [EasyOCR’s Cyrillic model selection](https://github.com/JaidedAI/EasyOCR/blob/master/easyocr/easyocr.py) identifies the model family used in this run.
'''
(out/'README.md').write_text(readme)
# Add matched conventional rows directly to existing reports, preserving their old results.
audit=[]
def enrich(path,panels,note=''):
 path=Path(path);s=path.read_text()if path.exists()else'# Matched conventional OCR results\n';marker='\n## Conventional OCR on the matching test material\n'
 if marker in s:s=s.split(marker)[0]
 link=os.path.relpath(out/'README.md',path.parent)
 s+=marker+'\n'+table(panels)+'\n'+note+'\nThese are new local OCR measurements, not substituted LLM results. Raw outputs, setup, scope adapters and per-target counts are in the [conventional OCR report]('+link+').\n';path.write_text(s);audit.append({'report':str(path.relative_to(ROOT)),'panels':[x[1]for x in panels],'status':'enriched with measured conventional baselines','note':note})
e=repo/'research/evaluations';three=[allpanels[1]];six=[allpanels[2]];letters=[allpanels[4]]
enrich(e/'comparison.md',[allpanels[0],allpanels[1]],'Compare only rows using the same material and CER mode; the 14 crops and three pages have different denominators.')
for d in ['gemma-pages-4-6-7','gemma-with-references','grok-three-example-pages']:
 pp=[('Page 4','diary-3-pages',['diary3-P04'],'reading'),('Page 6, final unknown word excluded','diary-3-pages',['diary3-P06'],'reading'),('Page 7','diary-3-pages',['diary3-P07'],'reading'),('All three pages','diary-3-pages',None,'reading')]
 if d=='gemma-pages-4-6-7':pp.append(('Common completed original plain-Gemma pages 4 and 6','diary-3-pages',['diary3-P04','diary3-P06'],'reading'))
 enrich(e/d/'README.md',pp)
enrich(e/'gemma-pages-4-6-7/page-7-plain-text-recovery/README.md',[('Page 7','diary-3-pages',['diary3-P07'],'reading')])
for d in ['page-06-assistant','page-06-gemini-vinnik']:enrich(e/d/'README.md',[('Page 6, final unknown word excluded','diary-3-pages',['diary3-P06'],'reading')],'The conventional baseline uses the frozen page-6 target region. The original contextual/external workflow cannot establish identical call inputs and effort.')
enrich(e/'six-page-skill-reference/README.md',six,'The existing CRNN and Kraken baseline results remain in the primary comparison table.')
enrich(e/'two-standalone-skills/README.md',[allpanels[3],allpanels[4]],'For any LLM row using fewer than all six diary pages or three excerpts, use matched-populations.json from the conventional report; it scores exactly that row’s matched target IDs.')
enrich(e/'rehand-popov/README.md',letters,'The conventional engines received the three frozen excerpt PNGs. Rehand used full pages; the text scopes match but the image inputs differ, so this is a practical workflow comparison.')
enrich(e/'crop-results/README.md',[allpanels[0]],'Selected single-line snippets only; existing CRNN/Kraken results are retained alongside these measurements.')
enrich(e/'sol-matched-pages-4-6-7/README.md',three)
for path,panel in [(ROOT/'outputs/hwr200-benchmark/README.md',allpanels[5]),(ROOT/'outputs/hwr200-expanded/README.md',allpanels[6]),(ROOT/'outputs/hwr200-expanded/provider-tests/README.md',allpanels[6])]:enrich(path,[(panel[0]+' — literal CER',*panel[1:]),(panel[0]+' — reading CER',panel[1],panel[2],'reading')],'The first row uses the historical principal literal CER; the second uses reading CER on the same material. The engines received no reference packet or skill.')
(out/'report-audit.json').write_text(json.dumps(audit,indent=2));print('Enriched',len(audit),'historical report files; exported raw results for 118 completed OCR tasks.')
