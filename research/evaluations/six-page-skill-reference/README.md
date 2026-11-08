# Skill and reference comparisons on six diary pages

Ollama is an experimental test backend. The tested Gemma setup does not justify recommending it for this diary. Use measured accuracy to select a model; a skill is not evidence that recognition improves.

One trial per condition on corrected comparison copies of pages **1, 2, 3, 5, 8 and 9**, scored 2026-11-02. Each complete cell uses the same **2,702 reference characters**. Reading CER = character insertions + deletions + substitutions divided by reference characters; lower is better. Case, punctuation and repeated whitespace are ignored; ё/е differences remain. Unknown markers on known text count as omissions. No target word is excluded.

| Model / setup | A: neither | B: skill only | C: references only | D: both |
|---|---:|---:|---:|---:|
| gemma4:12b / gemma | 25.87% (699/2702) | 28.53% (771/2702) | 70.39% (1902/2702) | 71.58% (1934/2702) |
| grok-4.7 / grok | Incomplete (2/6) | Incomplete (2/6) | Incomplete (3/6) | Incomplete (3/6) |
| deepseek-flash / deepseek-api-nonthinking | 18.17% (491/2702) | 18.36% (496/2702) | 16.88% (456/2702) | 18.17% (491/2702) |
| crnn / Automatic line segmentation | 26.05% (704/2702) | — | — | — |
| kraken-small / Automatic line segmentation | 31.13% (841/2702) | — | — | — |
| kraken-tiny / Automatic line segmentation | 40.86% (1104/2702) | — | — | — |
| glm-ocr:latest / GLM-OCR independent | 47.74% (1290/2702) | — | — | — |
| gemma4:12b / Gemma + GLM-OCR review B | 28.50% (770/2702) | — | — | — |
| gemma4:12b / Gemma + GLM-OCR review D | 71.61% (1935/2702) | — | — | — |

Supplemental rows place their independent score in the first column for compact display; they are not the primary A condition. Gemma + GLM-OCR review B/D means an additional image-grounded pass over the corresponding initial Gemma reading and an independent GLM-OCR candidate. It adds a model call.

Reference pages are **4, 6 and 7**, with corrected texts, supplied as full-page images. The unresolved last word on reference page 6 is marked unknown. These are page references, not a selective crop-retrieval test. The model may ignore them. A/B receive no reference images or labels. Corrected target text is evaluator-only. See the [frozen protocol and runnable handoff](../../handoffs/skill-reference-evaluation/README.md).

Gemma uses gemma4:12b through Ollama, temperature 0, 16,384 context, 2,048 output tokens. Grok uses grok-4.7, low reasoning, temperature 0.7, 4,096 output tokens. DeepSeek uses deepseek-flash with thinking disabled, temperature 0, 2,048 output tokens. All calls are stateless. Provider image handling and model settings differ, so this is a practical setup comparison, not a controlled estimate of model architecture effects.

Grok stopped after a 900-second read timeout on page 3 A. Its successful calls are retained, the timed-out call is an error, and unattempted cells are not scored as zero error. No complete six-page Grok aggregate is available. The reported cumulative xAI cost is $0.883464 including the earlier three-page experiment; billing for the timed-out request is unknown.

CRNN and Kraken share automatic Kraken line detection and original-pixel rectangular line crops. Segmentation omissions and ordering errors count in page CER; these rows do not isolate recognition from segmentation. No skill or reference labels were supplied to those recognizers.

These are corrected working comparison copies, not independently double-transcribed glyph-level ground truth. All source pages have been seen during project work; no untouched test set is claimed. One trial cannot establish a reliable general uplift. Compare complete conditions on this page set only; [other comparisons](../comparison.md) use different targets and skill snapshots.

The run files record requests, permitted image hashes, outputs, status and usage. Keys are not included. Raw encrypted reasoning is not published.

DeepSeek completed status: **finished**. Peak-rate usage estimate: **$0.028472**, under its $0.25 sub-budget. This is a conservative token-based estimate, not the provider's billed amount. See [official pricing](https://api-docs.deepseek.com/quick_start/pricing/).

Concrete page-3 errors can be checked in the prediction files:

- The corrected text includes «Ты меня расплакала и я теперь не могу успокоиться». DeepSeek A returns «или нет, у Распаканной и с петель», and B returns «или меньше, раскисает и теперь» before the surviving ending. Skill instructions do not resolve that phrase.
- The corrected text includes «Обезьянка такая хорошенькая». Gemma A reads «Объединя малая коронокоса»; DeepSeek C reads «Обедненка такая хорошенькая». Some words survive, but the subject is still wrong.
- Gemma C and D return the reference-page-7 story beginning «Юра ей … пойдем пешком в садик» instead of target page 3. This is visible reference copying, not improved target recognition. The cause inside the model/runtime has not been isolated.
