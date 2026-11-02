# GPT and DeepSeek diary API comparison

Planned; no API calls or scores yet. Credentials will be supplied later. No credentials belong in this repository or result files.

Use the same page 4, 6 and 7 target pixels and fixed user-confirmed reference texts as the local comparison. Exclude only page 6's unresolved final word. Preserve the odd child wording in the reference. Retain raw replies, exact prompts, image hashes, crop IDs, model names, settings, completion status, latency and reported token usage.

For each image-capable model, run plain reading, skill instructions only, and skill plus the same earlier-page reference images/profile. Keep output instructions, image processing and generation settings matched within that model. No corrected target-page text is supplied. Store every attempt, including incomplete replies; label any changed-prompt recovery separately. Compute per-page CER and summed-error aggregate CER, with literal CER and word errors retained separately.

DeepSeek's official [vision documentation](https://api-docs.deepseek.com/guides/vision/) says `deepseek-flash` accepts image input. Verify the account's available model and capabilities when credentials arrive. Test image reading directly; a text-only OCR reviewer, if tested, is a separate workflow.

For GPT, select and record the available image-capable API model at execution time. An API run must not be labeled as the earlier Sol agent test: model identity, runtime and interaction may differ.

Pages 8 and 9 remain review drafts. Do not add them to scored ground truth until the user confirms their wording. These pages have already been inspected; they are calibration material, not untouched test pages.
