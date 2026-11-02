# Gemma recognition on all three pages with usable ground truth

Gemma with the skill makes **12.4% fewer character errors** than Gemma without the skill on the common completed pages 4 and 6. Plain Gemma fails on page 7, so its three-page aggregate is not reported. Adding GLM-OCR makes **0.3% more character errors** compared with Gemma with the skill alone on the same pages 4 and 6. These are single-run measurements on known calibration pages.

CER ignores case and punctuation, normalizes whitespace and retains the distinction between ё and е. Lower is better. Fractions show character edits / reference characters. Only page 6's final unresolved word is excluded from each reading and reference.

| Workflow | Page 4 | Page 6 | Page 7 | All three pages |
|---|---:|---:|---:|---:|
| Gemma 4 12B without skill | 38.75% (198/511) | 31.42% (148/471) | Failed / not scored | **Failed / not scored** |
| Gemma without skill; page 7 plain-text recovery | 38.75% (198/511) | 31.42% (148/471) | 25.48% (119/467) | **32.09% (465/1449)** |
| Gemma 4 12B + skill | 33.07% (169/511) | 28.45% (134/471) | 21.41% (100/467) | **27.81% (403/1449)** |
| Gemma 4 12B + skill + GLM-OCR | 33.07% (169/511) | 28.66% (135/471) | 21.41% (100/467) | **27.88% (404/1449)** |
| GLM-OCR alone | 49.12% (251/511) | 44.37% (209/471) | 44.11% (206/467) | **45.96% (666/1449)** |

Plain Gemma on page 7 returns an invented date, then repeated blank lines until the token limit. Its response is incomplete JSON and is not scored. This is a failed attempt, not a missing experiment. All other stage completion statuses remain in run.json. The aggregate sums character errors and reference characters, rather than averaging the three percentages. Page 4 and page 7 have user-confirmed wording; page 6 has confirmed wording except its final word. Earlier pages have selected verified passages, not complete page-level references, so are not counted as additional complete test pages.

Each condition receives identical image pixels, no corrected target text, and no conversation history. The two skill conditions receive the same saved SKILL.md. No author profile or labeled reference crop is supplied: this comparison measures the instruction change, while the earlier Sol-assisted test also included author reference images. These are different assisted conditions.

Gemma reads independently before GLM-OCR. The combined condition receives the target image, skill, independent Gemma text and GLM-OCR text. Models are installed locally in Ollama; temperature 0, context 8192, generation limit 2048, Gemma thinking disabled, output JSON schema fixed across Gemma conditions. Calls are stateless and unload the model after each response. No fine-tuning or diary label changes occur.

The saved responses include uncertainty notes. Illegible markers count as omissions; they do not remove known text from scoring. The exact excluded page-6 suffix for every condition is recorded in page-6-exclusions.json, preserving all known preceding words. Model completion status and JSON validity are checked before scoring.

Examples from the actual saved readings:

- **Page 4, opening:**
  - Gemma 4 12B without skill: «— Бабушка, пошли ты на запенере ишь вон там - он когда ничего свалился на улице. — Борька, пошли пошли, давайте ей попрыгаем далеко и сыграем. - Чуть ли не шелм»
  - Gemma 4 12B + skill: «— Бабушка, почему ты на замену? Пишь я один раз — ты когда пойдет свиваться на улице. — Городок малeе хороший, давай мы еще поучимся немного и сыграем. — Чужое »
  - Gemma 4 12B + skill + GLM-OCR: «— Бабушка, почему ты на замену? Пишь я один раз — ты когда пойдет свиваться на улице. — Городок малeе хороший, давай мы еще поучимся немного и сыграем. — Чужое »

- **Page 6, opening:**
  - Gemma 4 12B without skill: «—Нана, если мы зарабатываем деньги, будет ли мне купить баночку варенья? Да, а зачем тебе? А баночку варенья есть. —(Если кобацу со сладкой молочной начинкой) м»
  - Gemma 4 12B + skill: «—Мама, если ты зарабатываешь деньги. Говорят, что мне купить баночку варенья? Да, и зачем тебе? А бери, вон туда, сиди. —(Если конбацу со сладкой многой начинко»
  - Gemma 4 12B + skill + GLM-OCR: «—Мама, если ты зарабатываешь деньги. Говорят, что мне купить баночку варенья? Да, и зачем тебе? А бери, вон туда, сиди. —(Если конбацу со сладкой многой начинко»

- **Page 7, opening:**
  - Gemma 4 12B without skill: «[Failed: incomplete repetitive output]»
  - Gemma 4 12B + skill: «Она бы - "Мальчик, пойдем поиграем в садик". - не хочу - Ты никогда ничего не хотела, - Мне, вера я всего хочу. Я горе - "Ну, Ваня, чего" - Мальчик, а что Ваня?»
  - Gemma 4 12B + skill + GLM-OCR: «Она бы - "Мальчик, пойдем поиграем в садик". - не хочу - Ты никогда ничего не хотела, - Мне, вера я всего хочу. Я горе - "Ну, Ваня, чего" - Мальчик, а что Ваня?»

All pages have already been inspected during this project. A single test on these three pages does not establish accuracy on unseen diary pages or prove which model is best in general. User-confirmed references preserve the wording, with editorial punctuation.

Evidence: [raw model replies and exact requests](run.json), [per-page and aggregate CER, literal CER and word errors](metrics.json), [excluded final word](page-6-exclusions.json), [skill used](skill-used.md). Image hashes, source coordinates and rotations match the [source manifest](../sol-matched-pages-4-6-7/manifest.json). Reference texts are frozen from the [same Sol test references](../sol-matched-pages-4-6-7/).

## Page 7 retry

An exact-settings retry repeats the incomplete-output failure. A separate plain-text recovery succeeds, with **25.48% CER** on page 7. See the [retry record and recovery score](page-7-plain-text-recovery/README.md). The original rows remain the first-attempt comparison. The additional recovery row mixes output protocols and includes the third page-7 attempt; it is not a controlled estimate of skill benefit.
