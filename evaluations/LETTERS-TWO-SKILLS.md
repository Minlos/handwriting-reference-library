# Evaluate automatic references separately from reading instructions

This is a prepared experiment, not a result. Do not start paid calls from this document. Current corrected Popov letters: L01 (11.04.43), L09 (22.01.44), L13 (10.12.43). They contain unresolved spans; corrections are contributor readings, not independent double transcription. Keep family-letter scans, answers and credentials out of public experiment packets unless their publication is separately authorized.

## Freeze the split before scoring

Use the other 14 Popov letters as the automatic extractor's uncorrected source collection. Exclude L01/L09/L13 and all their sides, corrected text and target-derived notes from extraction. Keep the four Gila letters separate: their authorship is unresolved. Run extraction in a fresh context with only allowed source images; old OCR outputs may contain knowledge from correction work and must not be silently reused. Automatic labels remain provisional. No coordinator corrections to the packet after examining target results.

Use the three corrected letters only as reading targets. The reading model sees their scans but never their corrections. The evaluator holds the frozen human texts. Exclude unresolved spans by predeclared shared line/region boundaries; preserve the known text on both sides. Do not simply delete all model uncertainty markers: an unknown prediction on known text remains an error. For this small pilot, score fully resolved lines where an internal unknown cannot be aligned reliably, and report omitted reference coverage. Do not claim whole-letter CER for partial-line scoring.

These letters and corrections have already been seen in this project. This is a pilot using isolated contexts, not an untouched benchmark. Later reserve newly corrected complete letters before revising the skills further.

## Reading comparison: four conditions

Freeze one reference packet produced automatically from the 14 uncorrected source letters using `extract-handwriting-references`. Do not provide extraction instructions to the downstream model.

| Condition | Reading skill | Frozen automatic reference packet |
|---|---|---|
| A | No | No |
| B | Yes | No |
| C | No | Yes |
| D | Yes | Yes |

Use `skills/read-handwriting/SKILL.md` for B/D, not the legacy combined root skill. A/C get the same neutral faithful-transcription request, without intentional weakening. Each target needs a fresh context for each condition; do not let a tested agent browse the repository or this plan. Supply reference crops as actual images with the same labels in C and D. Same model, image pixels, settings, base prompt, output schema and permitted tools in all cells. Keep no-reference conditions from creating a packet or browsing the source collection. Comparisons within a target image remain allowed.

A→B measures reading instructions without a packet; C→D measures reading instructions with the same packet. A→C and B→D measure the effect of the automatic packet. They do not, by themselves, establish that extraction instructions beat an ordinary extraction request.

## Extraction comparison: add the missing control

Run a neutral extractor on the same 14 sources: ask it to select and label useful same-writer handwriting examples, retaining locations and uncertainty. Run the extraction skill separately. Match source images, permitted tools, model, maximum calls/time and downstream image/token allowance. Preserve failures and actual usage; do not cherry-pick equal-sized packets after scoring. Both extractors may inspect all source images; neither receives target gold. Save both packets unchanged.

Read the same three targets with each packet and the same fixed reading skill. Together with B (no packet) and D (skill-built packet), add E (neutral-extractor packet). Optionally add F (neutral-extractor packet without reading instructions) for a complete three-by-two comparison. D versus E isolates the extraction-instruction workflow at the chosen downstream reader and budget. It is not a universal estimate of extractor quality.

Separately inspect extracted examples against source pixels: valid source bounds, clipped/blank crops, usable distinct forms, writer mixing, label errors and false human-confirmed labels. Human inspection for scoring must not silently repair the packets used in the automatic experiment. A corrected packet can be a separate upper-bound condition.

## Score and report limits

Save raw requests/replies, initial and final readings, packet/image/skill hashes, model settings, failures, elapsed time and cost. Counterbalance condition order. Aggregate CER by total character edits divided by total scored human-reference characters, not the mean of page percentages. Report each letter, scoring coverage, literal and normalized CER, omissions, altered names/numbers, plausible substitutions and correction time. Compare only matching completed target sets; show failed attempts separately.

For each valid pair, relative error reduction is `(baseline CER − compared CER) / baseline CER`; zero baseline is undefined. More self-reported confidence is not an accuracy metric. Repeat complete trials only within an explicit budget and keep first failures. Match extra reading calls when testing whether back-and-forth verification helps beyond simply spending another call.

A separate whole-collection condition may extract examples from unlabeled target scans too. Do not give it target corrections. Label it as collection-assisted reading and keep its scores separate from this held-out-letter split.
