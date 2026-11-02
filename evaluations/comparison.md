# Diary recognition: measured errors and the benefit of the skill

In the fresh three-page Sol comparison, skill plus earlier author references produces **41.8% fewer character errors** than plain Sol. This is the best tested condition on those three pages, not proof of the best possible model. Both agents received the same images and no corrected target text.

CER below ignores case and punctuation, normalizes spaces, and keeps ё distinct from е. It counts character substitutions, deletions and insertions divided by reference characters; lower is better. The fraction beside each percentage gives errors / reference characters. **Only the uncertain final word on page 6 is excluded from both texts.** Known words elsewhere remain scored even when the model marks them uncertain.

| Workflow | Evaluated material | CER ↓ |
|---|---|---:|
| Sol without skill | Pages 4, 6, 7; fresh test | 3.80% (55/1449) |
| Sol + skill + author references | Pages 4, 6, 7; fresh test | 2.21% (32/1449) |
| Original contextual assistant reading | Page 6; saved reading | 2.55% (12/471) |
| Gemini + Vinnik | Page 6; saved reading | 4.03% (19/471) |
| Gemma 4 12B without skill | Page 4 | 38.75% (198/511) |
| Gemma 4 12B + skill | Page 4 | 33.86% (173/511) |
| Gemma 4 12B + skill + GLM-OCR | Page 4 | 33.66% (172/511) |
| GLM-OCR | Page 4 | 49.12% (251/511) |
| Russian CRNN | 14 selected crops, pages 1–3 | 17.11% (39/228) |
| Kraken PP-OCRv6 small | 14 selected crops, pages 1–3 | 32.46% (74/228) |
| Kraken PP-OCRv6 tiny | 14 selected crops, pages 1–3 | 52.19% (119/228) |
| GLM-OCR | 14 selected crops, pages 1–3 | 89.91% (205/228) |

Concrete errors explain where the weaker readings lose meaning:

- **Fresh Sol, page 6:** plain Sol reads «Папа, еще одеяло и быстрее» instead of «Таня, ешь отдельно и быстрее». The assisted reading gets this sentence right. It also reads «ротик», where plain Sol tentatively reads «ромбик».
- **Fresh Sol still fails:** plain Sol correctly reads «заработаешь десять тысяч»; assisted Sol instead reads «заработаешь денег. Разве». Both replace the child's «хочила» with «хотела» and misread «валяй, иди». A better total score does not mean every sentence improves.
- **Gemma, page 4:** without the skill it reads «Бабушка, пошли ты на запенере»; with the skill, «Бабушка, поцелуй ты на затылке». The corrected reading is «Бабушка, почему ты на завтрак…». Adding GLM-OCR does not repair this passage. The two assisted Gemma results differ by only one character error over the page.
- **Gemini + Vinnik, page 6:** «заштриховать ромбик» replaces «заштриховать ротик»; «Танечка» replaces «Танюшка»; «папа» replaces «Таня» twice and «Мама» once.

## What the comparison supports

The fresh Sol result compares **skill plus 24 labeled author examples from pages 1–3** against a plain transcription task. It does not separate the benefit of the instructions from the benefit of the reference images. Page-level character error counts are plain/assisted: page 4, 22/10 out of 511; page 6, 23/14 out of 471; page 7, 10/8 out of 467. Totals sum errors and reference characters rather than averaging percentages.

Gemma's page-4 comparison uses identical target pixels, model, output schema, token limit and temperature. The plain run omits the skill system message; the saved assisted runs have no author examples or profile. The skill reduces Gemma's character errors by 12.6% in this one run, but errors remain frequent. Adding GLM-OCR reduces errors by only 0.6% relative to Gemma with the skill alone.

Rows using different material must not be ranked together. The 14 crops were hand-selected and contain much shorter text. The original assistant reading used conversation context and was subsequently corrected by the user; its reference is not independent of that workflow. Gemini + Vinnik's exact model version, prompt and prior context are unknown. Its result cannot establish a skill effect.

There are three usable page references here, not five complete references: pages 4 and 7 have confirmed wording; page 6 has confirmed wording except its final word. Pages 1–3 supply selected verified passages. Punctuation and dialogue layout are editorial, which is why the main table ignores them. Literal CER and word errors are retained in the result files.

All scans were previously inspected in this project. The two Sol agents have fresh contexts and were instructed to read only their allowed files; filesystem separation was by instruction, not operating-system enforcement. This is one trial on calibration pages, not an untouched benchmark or a promise of accuracy on the remaining diary.

Evidence: [fresh Sol results](sol-matched-pages-4-6-7/metrics.json), [plain Gemma result](page-04-gemma-plain/metrics.json), [assisted Gemma and GLM results](page-04-gemma-assisted/comparison.json), [original assistant](page-06-assistant/metrics.json), [Gemini + Vinnik](page-06-gemini-vinnik/metrics.json), [14-crop results](crop-results/).
