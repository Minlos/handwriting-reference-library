# Gemma with handwriting reference crops: three-page result

Gemma with the skill, seven earlier-page reference crops and a handwriting profile makes **10.9% more character errors** than the instruction-only Gemma run on the same pages 4, 6 and 7. Adding the GLM-OCR candidate makes **8.1% fewer character errors** compared with Gemma with the references alone. This is a single fixed-reference trial, not a search over examples or a claim about general accuracy.

CER below ignores case and punctuation, normalizes whitespace, and keeps ё distinct from е. Lower is better. Fractions show character errors / reference characters. Only the final unresolved word on page 6 is excluded from both texts. All known words remain scored, including words the model marks uncertain.

| Workflow | Page 4 | Page 6 | Page 7 | All three pages |
|---|---:|---:|---:|---:|
| Gemma + skill instructions only | 33.07% (169/511) | 28.45% (134/471) | 21.41% (100/467) | **27.81% (403/1449)** |
| Gemma + skill instructions + GLM-OCR | 33.07% (169/511) | 28.66% (135/471) | 21.41% (100/467) | **27.88% (404/1449)** |
| Gemma + skill + reference crops/profile | 37.18% (190/511) | 29.51% (139/471) | 25.27% (118/467) | **30.85% (447/1449)** |
| Gemma + skill + reference crops/profile + GLM-OCR | 30.14% (154/511) | 29.51% (139/471) | 25.27% (118/467) | **28.36% (411/1449)** |

The comparison keeps the same target pixels, model digest, frozen skill, generation settings and JSON output schema as the instruction-only experiment. The added inputs are exactly seven reference images, their user-confirmed labels, an earlier-page profile, and the text identifying each reference image. Temperature 0; context 8192; output limit 2048; thinking disabled; independent calls with no chat history. No user corrections from target pages 4, 6 or 7 are sent to the model. The OCR-assisted step reuses the saved GLM-OCR candidate for the identical target image.

Reference IDs: V001, V012, V013, V017, V019, V020, V022, all from pages 1–3. These are the seven images the fresh assisted Sol agent reported inspecting. Sol had a bank of 24 examples and selected those seven through tools; Gemma receives the same seven directly in one request. This aligns the actual reference images, but does not make the two model runtimes identical. Reference labels and profile are saved in run.json; crop hashes and source coordinates are retained. Labels apply only to their reference image.

The combined condition receives the actual target image and all reference images again, as well as the two candidate texts. No candidate agreement or model confidence is treated as verification. The user-confirmed labels and diary website text remain unaffected by these recognition suggestions.

Examples from the actual saved outputs:

- Page 4: «— Бабушка, пошли ты на заношенное ишьеньки или чай — мы когда пойдет свилянов на улице. — Городом пошел порядом, говорите, не порицайте, иначе и ограбайте. — Умная, умельни зову ме…»

- Page 6: «—Мама, если ты забарбатаешься где-то. Возьми мой личный кухонный бинный мешок. Да, я заберу тебе. А беляшку возьму еще. —(Если кобацу со сладкой многой начинкой). Мама, если он сил…»

- Page 7: «Она бы — «Мамочка, пойдем посидим в саду». — Не хочу. — Ты мамочка, ничего не хочешь. — Мне, вера я всего хочу. Я горе — «Ну, дай мне еще». — Мамочка, а что дайка? Мне мамочка сказ…»

Pages 4 and 7 have user-confirmed wording, and page 6 has one unresolved final word. Punctuation is editorial. All source pages were previously inspected in this project. The trial does not establish performance on unseen pages, and the reference selection was not optimized against these scores.

The older plain Gemma test failed on page 7 twice. Its successful plain-text recovery changed the generic instructions and output format, so its 32.09% three-page CER is a separately labeled recovery total, not the matched baseline for measuring the added reference crops.

Evidence: [raw model replies, exact prompts and reference metadata](run.json), [scores](metrics.json), [page-6 exclusion](page-6-exclusions.json), [instruction-only comparison](../gemma-pages-4-6-7/README.md).

## Conventional OCR on the matching test material

| Evaluated material | Tesseract 5.5.4, Russian best | EasyOCR 1.7.2, Cyrillic |
|---|---:|---:|
| Page 4 | 74.56% (381/511) | 82.58% (422/511) |
| Page 6, final unknown word excluded | 75.80% (357/471) | 87.69% (413/471) |
| Page 7 | 72.16% (337/467) | 82.66% (386/467) |
| All three pages | 74.19% (1075/1449) | 84.27% (1221/1449) |


These are new local OCR measurements, not substituted LLM results. Raw outputs, setup, scope adapters and per-target counts are in the [conventional OCR report](../conventional-baselines/README.md).
