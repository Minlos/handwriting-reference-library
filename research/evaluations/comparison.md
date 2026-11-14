# Diary recognition: measured errors and the benefit of the skill

The [six-page four-condition comparison](six-page-skill-reference/README.md) separately measures skill and reference effects on pages 1, 2, 3, 5, 8 and 9, including completed DeepSeek, Gemma and OCR tests. Do not pool its scores with the three-page table below.

In the fresh three-page Sol comparison, skill plus earlier author references produces **41.8% fewer character errors** than plain Sol. This is the best tested condition on those three pages, not proof of the best possible model. Both agents received the same images and no corrected target text.

CER below ignores case and punctuation, normalizes spaces, and keeps ё distinct from е. It counts character substitutions, deletions and insertions divided by reference characters; lower is better. The fraction beside each percentage gives errors / reference characters. **Only the uncertain final word on page 6 is excluded from both texts.** Known words elsewhere remain scored even when the model marks them uncertain.

| Workflow | Evaluated material | CER ↓ |
|---|---|---:|
| Sol without skill | Pages 4, 6, 7; fresh test | 3.80% (55/1449) |
| Sol + skill + author references | Pages 4, 6, 7; fresh test | 2.21% (32/1449) |
| Original contextual assistant reading | Page 6; saved reading | 2.55% (12/471) |
| Gemini + Vinnik | Page 6; saved reading | 4.03% (19/471) |
| Gemma 4 12B without skill | Pages 4 and 6 completed; page 7 failed | No three-page total |
| Gemma without skill; page 7 plain-text recovery | Pages 4 and 6 original JSON; page 7 recovery on third attempt | 32.09% (465/1449) |
| Gemma 4 12B + skill | Pages 4, 6, 7; local test | 27.81% (403/1449) |
| Gemma 4 12B + skill + GLM-OCR | Pages 4, 6, 7; local test | 27.88% (404/1449) |
| Gemma + skill + reference crops/profile | Pages 4, 6, 7; local test | 30.85% (447/1449) |
| Gemma + skill + reference crops/profile + GLM-OCR | Pages 4, 6, 7; local test | 28.36% (411/1449) |
| Grok 4.7 + three example pages | Pages 4, 6, 7; examples are pages 1–3 | 9.45% (137/1449) |
| Grok 4.7 + same examples + skill | Pages 4, 6, 7; examples are pages 1–3 | 9.11% (132/1449) |
| GLM-OCR | Pages 4, 6, 7; local test | 45.96% (666/1449) |
| Russian CRNN | 14 selected crops, pages 1–3 | 17.11% (39/228) |
| Kraken PP-OCRv6 small | 14 selected crops, pages 1–3 | 32.46% (74/228) |
| Kraken PP-OCRv6 tiny | 14 selected crops, pages 1–3 | 52.19% (119/228) |
| GLM-OCR | 14 selected crops, pages 1–3 | 89.91% (205/228) |

Concrete errors explain where the weaker readings lose meaning:

- **Fresh Sol, page 6:** plain Sol reads «Папа, еще одеяло и быстрее» instead of «Таня, ешь отдельно и быстрее». The assisted reading gets this sentence right. It also reads «ротик», where plain Sol tentatively reads «ромбик».
- **Fresh Sol still fails:** plain Sol correctly reads «заработаешь десять тысяч»; assisted Sol instead reads «заработаешь денег. Разве». Both replace the child's «хочила» with «хотела» and misread «валяй, иди». A better total score does not mean every sentence improves.
- **Gemma, page 6:** without the skill it reads «Мне надо "заткнуться ротчик"» instead of «Мне надо “заштриховать ротик”». See the all-page Gemma comparison for raw examples from each condition.
- **Gemini + Vinnik, page 6:** «заштриховать ромбик» replaces «заштриховать ротик»; «Танечка» replaces «Танюшка»; «папа» replaces «Таня» twice and «Мама» once.

## What the comparison supports

The fresh Sol result compares **skill plus 24 labeled author examples from pages 1–3** against a plain transcription task. It does not separate the benefit of the instructions from the benefit of the reference images. Page-level character error counts are plain/assisted: page 4, 22/10 out of 511; page 6, 23/14 out of 471; page 7, 10/8 out of 467. Totals sum errors and reference characters rather than averaging percentages.

Gemma's three-page comparison uses identical target pixels, installed models, output schema, token limit and temperature. The skill conditions have no author examples or profile. On the common completed pages 4 and 6, the skill produces 12.4% fewer character errors than plain Gemma; adding GLM-OCR produces 0.3% more character errors compared with Gemma with the skill alone on those same two pages. Plain Gemma fails on page 7; no three-page plain CER is reported. See the [per-page Gemma table](gemma-pages-4-6-7/README.md).

Rows using different material must not be ranked together. The 14 crops were hand-selected and contain much shorter text. The original assistant reading used conversation context and was subsequently corrected by the user; its reference is not independent of that workflow. Gemini + Vinnik's exact model version, prompt and prior context are unknown. Its result cannot establish a skill effect.

There are three usable page references here, not five complete references: pages 4 and 7 have confirmed wording; page 6 has confirmed wording except its final word. Pages 1–3 supply selected verified passages. Punctuation and dialogue layout are editorial, which is why the main table ignores them. Literal CER and word errors are retained in the result files.

All scans were previously inspected in this project. The two Sol agents have fresh contexts and were instructed to read only their allowed files; filesystem separation was by instruction, not operating-system enforcement. This is one trial on calibration pages, not an untouched benchmark or a promise of accuracy on the remaining diary.

Evidence: [fresh Sol results](sol-matched-pages-4-6-7/metrics.json), [all-page Gemma and GLM results](gemma-pages-4-6-7/metrics.json), [original assistant](page-06-assistant/metrics.json), [Gemini + Vinnik](page-06-gemini-vinnik/metrics.json), [14-crop results](crop-results).

An exact page-7 plain-Gemma retry also fails. A [plain-text recovery](gemma-pages-4-6-7/page-7-plain-text-recovery/README.md) completes with 25.48% CER. This uses changed generic instructions and no JSON schema, so it is reported separately from the original comparison.

The completed [Gemma reference-crop test](gemma-with-references/README.md) produces 10.9% more character errors than the matched instruction-only run. It supplies the seven earlier-page images actually inspected by assisted Sol, plus their labels and the earlier-page profile; target-page labels are withheld.

The [Grok API test](grok-three-example-pages/README.md) keeps the same three full example pages and verified excerpts in both conditions. The added skill yields 3.6% fewer character errors in one trial, with a regression on page 7. All six calls together cost $0.402454. This isolates instructions given examples; Sol's earlier comparison also changed reference access.

## Conventional OCR on the matching test material

| Evaluated material | Tesseract 5.5.4, Russian best | EasyOCR 1.7.2, Cyrillic |
|---|---:|---:|
| 14 selected diary crops | 96.93% (221/228) | 91.67% (209/228) |
| Diary pages 4, 6, 7 | 74.19% (1075/1449) | 84.27% (1221/1449) |

Compare only rows using the same material and CER mode; the 14 crops and three pages have different denominators.
These are new local OCR measurements, not substituted LLM results. Raw outputs, setup, scope adapters and per-target counts are in the [conventional OCR report](conventional-baselines/README.md).
