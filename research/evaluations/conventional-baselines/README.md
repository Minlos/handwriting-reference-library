# Conventional OCR on the historical comparison sets

These tests add conventional OCR baselines to the existing handwriting comparisons. Each engine received the same frozen source image bytes as its corresponding test panel. Neither engine received reference transcriptions, author examples, skill instructions or another recognizer’s output. The collection downloads are separate from these evaluations.

Tesseract and EasyOCR completed all 59 distinct input/scope tasks without recognition-call errors. The seven scoring panels reuse overlapping inputs; they must not be added together or pooled into one accuracy figure. Empty OCR output is scored as omissions, not dropped. Fractions below are character edits / normalized reference characters. Lower CER is better.

| Evaluated material | Tesseract 5.5.4, Russian best | EasyOCR 1.7.2, Cyrillic |
|---|---:|---:|
| 14 selected diary crops | 96.93% (221/228) | 91.67% (209/228) |
| Diary pages 4, 6, 7 | 74.19% (1075/1449) | 84.27% (1221/1449) |
| Diary pages 1, 2, 3, 5, 8, 9 | 75.54% (2041/2702) | 83.75% (2263/2702) |
| Standalone reading/extraction: diary | 75.54% (2041/2702) | 83.75% (2263/2702) |
| Three Popov excerpts | 79.32% (468/590) | 83.56% (493/590) |
| HWR200 first pilot: 2 scans | 80.76% (2564/3175) | 87.06% (2764/3175) |
| HWR200 expanded: 31 scans / 10 documents | 77.23% (26661/34520) | 88.36% (30502/34520) |

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

## Reproducing the scores

The source/ directory preserves the scripts used for this run and the historical HWR metric implementation. These are execution snapshots from the collection workspace, not a standalone installer: their relative paths expect work/conventional-baselines, outputs/hwr200-expanded and the frozen historical fixtures. inputs.json records workspace-relative source paths and SHA256 hashes. The 82.9 MB of source image files and model weights are not duplicated in this report folder. Inference scripts read inputs.json only; scoring scripts read evaluator.json separately. To audit scores without running recognition again, use the retained raw outputs, frozen references and metric implementation.
