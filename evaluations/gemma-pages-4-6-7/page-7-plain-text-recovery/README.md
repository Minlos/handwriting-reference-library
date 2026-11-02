# Page 7: exact retry and plain-text recovery

The original plain-Gemma run and one exact-settings retry both hit the 2048-token limit while repeating line-break codes. They never completed the JSON response. The first began with an invented date; the exact retry began with `1.`. We do not know the underlying model cause. Their raw replies are preserved.

A third attempt uses generic plain-text transcription instructions and removes the JSON schema. It produces a complete reading. No skill, author references, corrected words or earlier model readings are supplied. Image pixels, model and generation settings remain the same. Because both the prompt and output format change, this is a separately labeled recovery test.

| Result | Character errors / reference characters | Reading CER |
|---|---:|---:|
| Page 7, plain-text recovery | 119 / 467 | 25.48% |
| Pages 4 and 6 original plain readings + page 7 recovery | 465 / 1449 | 32.09% |

Reading CER ignores case and punctuation, normalizes whitespace and keeps ё distinct from е. All page-7 words are scored; it has no excluded final word. The unresolved final word on page 6 remains excluded in its original score. The combined row mixes output protocols and includes a retry; it must not be used as a controlled estimate of skill benefit.

Examples of remaining errors in the recovery:

- «Машонка, пойдем печенье в садике» instead of «Танечка, пойдем пешком в садик».
- «Ку, Ваняч» instead of «Ну, валяй, иди».
- «пущен морж» instead of «гутен морген».

Evidence: [exact retry](../page-7-plain-retry/retry.json), [plain-text recovery request and response](recovery.json), [reading](reading.txt), [metrics](metrics.json). The first failed attempt remains in the parent run.json unchanged.
