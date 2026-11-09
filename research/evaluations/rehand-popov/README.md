# Rehand on corrected Popov excerpts

**Rehand is competitive on this small pilot.** Its saved full-page OCR produces **14.07% CER (83 edits / 590 reference characters)** on the same three resolved text regions used by the standalone-skill experiment. It is one character edit behind Astra with the reading skill and raw references, and seven edits ahead of Sol in that condition. This is not evidence of a reliable winner.

| Scored excerpt | Character edits / reference characters | CER ↓ |
|---|---:|---:|
| 11.04.43 — opening, L01 | 22 / 223 | 9.87% |
| 22.01.44 — mood statement, L09 | 15 / 31 | 48.39% |
| 10.12.43 — opening, L13 | 46 / 336 | 13.69% |
| **All three excerpts** | **83 / 590** | **14.07%** |

For context, the same scored regions in the [standalone-skill pilot](../two-standalone-skills/README.md) give Sol without instructions/references 18.47%, Sol with both 15.25%, Astra without both 17.46%, and Astra with both 13.90%. Those are different input protocols: Rehand received **1350×1800 whole-page images**, while the LLMs received excerpts cropped from 1800×2400 viewing images. Extra context and resolution can both affect accuracy. This is a comparison on matching text scopes, not identical pixels or a controlled estimate of model effects.

## How saved output was scored

No new upload, API call or paid inference was made. We used the completed saved Rehand responses for I01, I18 and I26 and verified the SHA-256 of each actual submitted image. The provider/model version is not identified in these saved responses.

Word boxes are mapped geometrically to the existing excerpt coordinate frame. Select boxes by their centers and keep the provider's original order; do not rewrite words, filter by confidence or align words against the answer text. For L09 the task requests the bottom complete line and excludes partial neighboring ink. Its scoring region is the lower half of the existing crop. An initial boundary check showed a box from the partial upper line crossing the broader region; that box was excluded by the geometric lower-half rule, not by matching its text. The total edit count happened to remain unchanged.

The reference is the contributor's corrected wording. Unresolved passages are outside these predefined excerpt targets. Normalization is exactly the existing pilot's CER function: NFC, case and punctuation ignored, repeated whitespace collapsed, ё/е distinct. Edits and denominator are summed, not averaged across excerpts. These are **excerpt scores**, not whole-letter CER, and the material has already been reviewed during the project.

[metrics.json](metrics.json) includes unchanged selected OCR text, reference text, source/response hashes, selected box indices, original box coordinates, mapping dimensions, reading CER and literal CER. The raw full-page responses remain locally archived; only the relevant selected boxes are published here.

## Example and practical implication

For «Сейчас здоров, настроение ничего.» Rehand returns **«здоров ремя ничего»**. It omits «Сейчас» and damages «настроение», but preserves more of the phrase than several LLM baseline readings. It still needs human correction. On L01 it changes «Александра Петровна» to «Александр, Петрович» and «Целую Вас всех» to «Услую все всех».

Rehand is worth keeping as an independent candidate reader for these letters. The next fair test should supply identical whole-page images to Rehand, Sol and Astra, score the same verified regions, repeat trials where applicable, and measure correction time. The present result does not establish accuracy on the unverified letters or prove that adding Rehand to an LLM will improve the combined result.

## Reproduce locally

Run from the repository root, with the archived letter folder available:

```sh
python3 research/tools/score_rehand_popov.py --letters-dir /path/to/letters-new-author --output /path/to/new-metrics.json
```

This reads saved OCR boxes and image files only; it makes no network requests.
