# Ready OCR systems versus Sol and Astra on nine public HWR200 scans

The question is whether a general LLM, with or without the reading skill, is competitive with ready OCR/HTR systems on identical public scans. This is a selection study on nine scan files from nine writers and eight distinct source texts. Success means fewer character edits against the same supplied references, with failures, runtime and access requirements retained.

**Plain Astra has the lowest CER among the completed configurations.** Neither model improves with the reading skill in this run. Transkribus model148545 is the strongest completed ready OCR/HTR configuration. Rehand returned server errors and remains unscored, so the overall selection is still open.

| System | Completed pages | Literal CER | Reading CER | Character edits / reference characters |
|---|---:|---:|---:|---:|
| Astra, plain | 9/9 | 9.81% | 9.13% | 2757 / 28109 |
| Astra + reading skill | 9/9 | 15.30% | 14.07% | 4302 / 28109 |
| Sol, plain | 9/9 | 19.55% | 18.81% | 5496 / 28109 |
| Transkribus Russian generic handwritten and typed 1 (148545) | 9/9 | 20.52% | 19.27% | 5768 / 28109 |
| Sol + reading skill | 9/9 | 21.22% | 19.58% | 5965 / 28109 |
| Russian CRNN | 9/9 | 25.99% | 24.73% | 7306 / 28109 |
| Kraken-small | 9/9 | 33.14% | 32.36% | 9314 / 28109 |
| Apple Vision | 9/9 | 60.74% | 59.97% | 17074 / 28109 |
| PaddleOCR 3.7.0 / PP-OCRv5 Russian | 9/9 | 70.35% | 70.09% | 19774 / 28109 |
| Tesseract 5.5.4 | 9/9 | 81.84% | 79.63% | 23004 / 28109 |
| EasyOCR 1.7.2 | 9/9 | 86.93% | 84.65% | 24435 / 28109 |
| Rehand | 0/9 | Not ranked | Not ranked | Incomplete |
| Calamari | 0/9 | Not ranked | Not ranked | No applicable checkpoint identified |

All completed aggregates use the same 28,109 literal reference characters, or 26,988 characters after reading normalization. Literal CER preserves case and punctuation; both modes use NFC and whitespace collapse. Reading CER additionally casefolds and removes Unicode punctuation, retaining ё. Lower CER is better. The combined value sums edits and reference characters; it is not a mean of page percentages. Incomplete systems receive no aggregate rank. These are disagreements with published source texts, not independently audited counts of visual reading errors.

## Identical originals prevent the earlier full-page/crop mismatch

Every system receives the exact original full-scan bytes in inputs/, with the same SHA256 recorded in inputs.json and its output. There is no parent-supplied resizing, rotation, crop, reference packet or candidate OCR text. Each OCR pipeline may perform its own internal detection and resizing; those are parts of the tested system. Sol and Astra run in separate fresh agents without parent history. Plain agents receive an ordinary faithful-transcription request. Skill agents receive the frozen reading-skill-snapshot.md, save initial/final predictions and describe actual pass coverage. No evaluator text is supplied to any recognizer.

This compares whole workflows, not equal compute or a fixed number of image views. There is one run per model condition; repeated-run variation is unmeasured. Agents share context across their nine assigned pages but are instructed to keep writers separate. Model names are the requested agent model identifiers recorded in the dispatch and outputs, not a provider API billing record. No paid OCR/LLM API calls were made in this study; host subscription usage is not monetized here.

Kraken-small and Russian CRNN use shared automatic Kraken baseline segmentation followed by axis-aligned original-pixel line regions. Detection failures remain in page CER. Tesseract uses Russian tessdata_best, OEM1 and PSM3. EasyOCR uses CRAFT plus cyrillic_g2 with ru/en on CPU. PaddleOCR uses its official PP-OCRv5 Russian selection, resolving to eslav_PP-OCRv5_mobile_rec, with page detection, upright input, no document unwarping and CPU inference. Apple Vision uses accurate CPU recognition, ru-RU/en-US and disabled language correction. Versions, settings, model hashes, raw outputs and source snapshots accompany this report. Native Apple service errors from a sandboxed setup attempt were excluded; those pages were rerun successfully outside the sandbox.

## Nine writers do not establish a universal winner

The sample is all nine complete single-scan documents in the locally collected pinned HWR200 subset, selected from metadata before recognition. The writers are 009, 015, 035, 037, 040, 065, 072, 080 and 153. Writers037 and072 copy the same original2 text. Resolution ranges from 584×800 to 2564×3500, with dense and faint writing. This selection favors single-scan documents and is not a random sample of the full dataset. It contains no family diary or letters. It also overlaps earlier evaluation material for writer009 and source text families; it is a selection sample, not an untouched confirmation set.

References are upstream full-document texts. Copied wording can differ from those texts. Scan/reference correspondence was visually spot-checked, but the references were not fully audited character by character. Labels remain frozen for every system. We do not silently correct them to favor a prediction. The paired writer resampling in paired-uncertainty.json measures sensitivity to these selected writers, not general population certainty; two writers also share a source text. A fresh confirmation set and stronger service results are required before selecting a permanent winner.

## Transkribus is matched; Rehand still has no result

Rehand received the exact original first scan, but the request timed out after150 seconds. Separate website/endpoint checks and an alternate HTTP client also timed out. Browser uploads returned the same server error on writer009, writer015 and the larger2244×3072 writer035 scan. No successful Rehand transcription was returned. The saved older Popov score used different image inputs and is not imported into this table. This is an access failure, not a measured high CER.

Transkribus was confirmed by the user as the registration-required candidate. The nine identical files were uploaded as one document in Chrome, after the user authorized that browser exception and enabled local-file upload access. Russian generic handwritten and typed 1 (model148545) completed pages1–9 in job32001209, document20272181, collection2599539, in390.473 seconds. Nine credits were deducted from the observed50-credit balance. Its export job32001301 supplied nine unedited page TXT files, Page XML and the input images. All nine exported-image SHA256 hashes match the shared input originals exactly. No subscription upgrade or purchase was made. This tests one identified public Russian model, not every Transkribus configuration. Text TitanII was locked on the free account and was not tested; no claim about that premium model is supported. Published validation CER on a model card is not a score on our sample.

Calamari is a line-recognition engine. Its official model catalog did not supply an identified Russian handwriting checkpoint for this test. It is not assigned a fabricated score or run with an unrelated Latin/Fraktur model. This unresolved suitability item is recorded separately from completed inference.

## Sources and reproducibility

Dataset: [AntiplagiatCompany/HWR200](https://huggingface.co/datasets/AntiplagiatCompany/HWR200), revision366a882a2b8d043d437126d2878bd3812ec55a94, declared Apache-2.0. Credit Ivan Potyashin, Mariam Kaprielova, Yury Chekhovich, Alexandr Kildyakov, Temirlan Seil, Evgeny Finogeev and Andrey Grabovoy, “HWR200: New open access dataset of handwritten texts images in Russian” (2023). The nine inputs are unmodified source scans; dataset text and images remain separate from the skill license. Public benchmark exposure during model training is unknown.

Other primary references: [Calamari model catalog](https://github.com/Calamari-OCR/calamari_models), [Transkribus public Russian models](https://www.transkribus.org/models/russian-generic-handwriting), [PaddleOCR pipeline documentation](https://www.paddleocr.ai/main/en/version3.x/pipeline_usage/OCR.html).

inputs.json contains original hashes and paths; evaluator/gold.json contains frozen labels; metrics.json contains per-page predictions and exact counts; raw/ retains recognizer records. source/ preserves the run scripts as workspace execution snapshots; model installation and host agent calls are not a one-command reproducible environment. The standalone metric implementation is included for rescoring saved predictions. Future ordinary recognition should use the retained leaders, while other LLM experiments should isolate skill effects.
