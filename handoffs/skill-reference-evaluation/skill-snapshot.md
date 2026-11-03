---
name: handwriting-reference-library
description: Transcribe handwriting from image evidence, use author-specific references when useful, and maintain source-located examples from human corrections. Applies across LLM hosts; distinguish visual reading from text-only OCR review.
---

# Handwriting reference library

## Match the task to available capabilities

The host supplies images, permitted references and any file or OCR tools. A vision model can read supplied images without a particular product mode. A text-only model may coordinate OCR or review candidate text, but must identify that role and must not claim to have visually inspected handwriting it cannot see. If the required image evidence is missing, state what is missing rather than inventing a reading.

Creating crops, saving a library and checking coordinates require an executable host or tool-using agent. Do not claim those actions, a mode switch or a reference lookup unless they actually happened. Read [HOST.md](HOST.md) when building or updating files; do not inject the host manual into every transcription prompt.

## Read the target before resolving uncertainty

Start with clearly legible words and visible letter connections. Use one author's examples together only when authorship is supported. Preserve the written language, unusual child forms, spelling and grammar; fluent or conventional wording is not evidence of the letters. Do not reconstruct missing strokes.

For uncertain spans, distinguish a tentative reading from an unread span using the host's requested notation. Keep known text even when nearby words are uncertain. Follow the requested output format; put provenance or commentary separately when requested so it does not become part of the transcript.

## Use references selectively, not compulsorily

References are optional evidence. An agent with tools may retrieve a few relevant verified examples from the permitted library. In a single model call, compare only the reference images the host actually supplied. Reading labels or a profile without seeing the corresponding images is not visual comparison.

Prefer examples sharing a visible letter shape or connection with the uncertain region. Record only IDs actually compared and the visible support when requested. A shared prefix does not establish a whole word. If references are irrelevant, conflicting or make the reading less clear, ignore them and return to the target; keep unresolved text uncertain. Do not force an interpretation to match a reference.

Profiles are hypotheses tied to source examples, not rules that determine the target answer. The host chooses reference quantity and presentation; fewer examples are not assumed to be better until tested.

## Treat OCR and confidence as evidence to check

An OCR result is a candidate, not ground truth. When the workflow includes OCR review, check candidate differences against the target pixels. Preserve unusual wording when supported; do not repair the text into plausible adult prose. Candidate agreement and model confidence do not verify a label. Keep the independent reading when the host asks for a before/after comparison.

## Preserve confirmation boundaries

`verified` means wording explicitly confirmed or corrected by a human, with its source recorded. It does not certify every glyph or punctuation mark. `provisional` means a visually supported but unconfirmed reading. Keep unresolved alternatives separate. A correction to one fragment does not confirm the rest of its page.

After corrections, keep the supplied reading distinct from independently improved recognition. Return to related unresolved passages when relevant, and report only changes actually supported by images. Do not claim that reference growth itself improves accuracy or changes model weights.

## Evaluate and share without changing the evidence

Keep whole reference pages separate from target pages. Do not supply corrected target text, overlapping target crops, error logs or target-derived profiles to a blind reading. Preserve failures and changed-prompt retries separately. Use the same images and generation/output settings when testing a condition change. Instructions, references and OCR can each help or hurt; no fixed accuracy is promised.

This is plain Markdown for any suitable LLM host. Optional local backend instructions are in [LOCAL.md](LOCAL.md) and [OLLAMA.md](OLLAMA.md). Model suggestions remain subject to visual and human review.
