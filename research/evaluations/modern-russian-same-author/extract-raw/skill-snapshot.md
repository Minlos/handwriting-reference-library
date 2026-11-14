---
name: extract-handwriting-references
description: Select and label traceable handwriting examples from a permitted collection, including uncorrected scans, for another reader to use. Use when building an author-specific reference packet rather than transcribing target letters.
---

# Extract handwriting references

Produce a compact, traceable packet of handwriting examples. This skill selects evidence; it does not deliver a final transcription of the target documents. It works independently of a particular model, OCR service or companion skill.

## Survey before selecting

Provisionally read all permitted source images before selecting examples. Record image coverage and likely writers; keep uncertain writer matches separate. Envelopes and repeated names can help identify writers but do not establish an attribution by themselves. If access or a stated budget prevents full coverage, report the actual coverage.

Use recurring words, letters, joins and endings to find clear examples across the collection. Existing OCR may offer candidates; agreement between tools is not verification. With no human-corrected text, assign provisional labels only. Do not reconstruct a label from what a sentence ought to say. Reject an ambiguous example rather than filling the packet with unreliable labels.

Select examples that cover distinct useful shapes or an explicitly supplied visual difficulty. Avoid many near-duplicates. There is no fixed number of examples or contributing source pages. Respect an explicit image/token budget, and record which examples were omitted to meet it.

## Keep each example auditable

Use original pixels for crops. Inspect each actual crop, including its complete beginning and ending; re-crop clipped words and reject blank or irrelevant regions. Preserve source image ID, original dimensions, SHA-256 where tools permit, rotation, and crop bounds with a stated coordinate convention. For an unrotated image, use integer `xyxy` pixels with top-left origin and exclusive right/bottom edges. For a rotated crop, also state the transform and the coordinate frame. Do not fabricate coordinates or claim saved crops when the host cannot create them.

For every example, provide the image or directly accessible region, proposed label, writer ID, source location, label status, and unresolved alternatives. `human-confirmed` applies only to wording actually supplied or confirmed by a person, with provenance; `provisional` applies to model readings. Preserve the person's question marks. A clear prefix is not evidence for the whole word. Context may explain a choice but cannot supply absent strokes.

Check proposed labels again against source images and recurring same-writer forms. Save revisions and rejected examples where they explain a material uncertainty. Stop after a full review produces no supported label changes, or at the stated limit; report unresolved examples. Do not silently promote automatic labels to confirmed labels.

## Hand off evidence, not target answers

The packet contains examples and their provenance, source coverage, uncertain writer matches and any selection limits. A reader may ignore an example that conflicts with the target strokes. Keep examples separate from recognition instructions so they can be tested independently.

In ordinary collection work, examples may come from any permitted image, including the current target. In a held-out-letter test, use only the assigned source letters: no target crops, target corrections, target-derived profile or answers from the scoring files. Freeze one packet before reading the targets, and supply the identical packet to compared reading conditions. If the host cannot expose an actual image to the reader, label that setup unsupported rather than presenting text labels as visual references.

The optional `test-material/` folder contains exercises and evaluator answers, not runtime instructions. Do not load its answers during a blind test. This workflow does not authorize external uploads or paid calls.
