---
name: read-handwriting
description: Transcribe handwriting by alternating contextual hypotheses with checks of visible letters and complete lines. Can use a supplied reference packet, but does not require or automatically build one.
---

# Read handwriting against the image

Produce a faithful transcription with visible uncertainty. Use the supplied scans and, optionally, a supplied handwriting reference packet. Work with any suitable vision model or tool-using host. A text-only host may review OCR candidates but must not claim to inspect letters it cannot see.

## Read, compare, return to the strokes

Make an initial reading of all supplied target pages, including initially difficult passages. Record missing sides, uncertain page order and writer changes. Preserve spelling, unusual words, child language and incomplete sentences. Do not replace them with more familiar prose.

For an uncertain span, propose a small set of readings from visible shapes and context. Compare each against the complete word: length, beginning, ending, joins and position in the line. Then reread the surrounding sentence and return to the image. Context proposes a hypothesis; the target strokes decide whether it survives. A fluent sentence is not sufficient evidence. If no reading is supported, retain an unknown span rather than choosing the most plausible story.

When references are supplied, compare relevant same-writer forms with the target. Check their provisional labels against their own images; ignore a misleading example. Do not copy a reference passage into the target or treat an author's recurring word as proof it appears here. Without a packet, use the target's own visible repetitions when permitted. This skill does not automatically invoke extraction, fetch other documents or build a saved library.

Available OCR readings are independent hypotheses. Check disagreements against the image, not by majority vote. Keep independent outputs when the task is an experiment. Do not call agreement or model confidence a verified transcription.

## Revisit the whole supplied text

Use supported discoveries to reread all supplied target pages, including passages first considered clear. Keep materially changed spans and the image evidence for them. Repeat while a full pass yields supported changes; stop after a complete pass yields none, or at a stated time/cost or access limit. State actual coverage rather than claiming a complete collection pass after reading a selection.

Before presenting a reading as visually checked, inspect its complete final lines on the scan, including their beginnings and endings. Re-reading text or viewing a PDF layout is not this check. Mark remaining ambiguities and partial lines. A second look is a procedure, not proof that a reading is correct.

## Preserve the correction boundary

Record user corrections verbatim and separately from independent predictions. A corrected fragment does not confirm the rest of a page. Preserve user question marks and unusual spelling. When a user identifies a letter by date or opening, show its full current transcription with unresolved spans marked. Do not claim a correction was independently recognized or visually verified unless that separate check actually happened.

Follow the task's output notation. Report missing images honestly. In an evaluation, receive only the assigned target scans, instructions and reference packet: never evaluator answers, previous errors or target corrections. Save initial and final readings, completion status, actual pass coverage and unresolved spans without exposing hidden chain-of-thought; brief source-tied change notes are sufficient.

The optional `test-material/` folder is for testing only and includes evaluator answers. Do not load it during ordinary transcription or expose its answers in a blind test. This skill makes no guaranteed accuracy claim and authorizes no external uploads or paid calls.
