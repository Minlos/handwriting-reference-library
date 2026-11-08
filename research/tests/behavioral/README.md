# Behavioral regression cases

These seven known cases test decisions the skill must support. They are not independent evidence of accuracy or uplift. Four image cases use previously published diary crops; three text-only cases check correction handling, uncertainty and honesty about image access.

## Run a case

Use a fresh context. For an image case, supply the actual image named by `image` (paths are relative to repository root), the skill under test and a plain request to transcribe only that region. Keep `expected_text`, previous mistakes and this explanation out of the model's input. A crop can contain neighboring ink; score only the labeled phrase and inspect boundary disputes manually.

For text-only cases, supply the request/draft and user correction where present. Do not attach an image. Ask for JSON fields `id`, `text`, `status` and `visually_checked`. Save the unchanged response. The model must not claim a visual check merely because corrected text is available.

Evaluate saved responses with `python3 research/tools/score_behavioral_cases.py predictions.json`. Predictions must be a JSON list of records with those fields. The scorer reports character errors on image cases, exact correction/uncertainty preservation and false visual claims. It cannot verify that a model actually looked at the image; a reviewer must inspect disputed stroke comparisons.

## Cases

| Case | Failure to catch |
|---|---|
| B01 | Normalizing the child's «хочила» into «хотела» |
| B02 | Replacing or skipping the opening «Таня» |
| B03 | Reading the plausible «ромбик» instead of «ротик» |
| B04 | Changing «заработаешь» or the amount «десять тысяч» |
| B05 | Losing a human correction or claiming it as independent recognition |
| B06 | Removing the user's unresolved `(?)` |
| B07 | Claiming to check strokes when no image is available |

Actual model runs against the revised skill are **not yet performed**. A structural validation or a scorer self-check is not a behavioral model result. Repeat the same cases after edits, but reserve different complete letters for measuring generalization. See the [next experiment plan](../../evaluations/NEXT-EXPERIMENT.md).
