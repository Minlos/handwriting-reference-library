---
name: read-handwriting
description: Transcribe handwriting faithfully by checking uncertain readings against complete visible words and lines. Works with suitable vision models and optionally uses supplied same-writer examples; does not extract references automatically.
---

# Read handwriting against the image

Use the supplied images. A text-only model may compare OCR readings but cannot claim to inspect handwriting. Identify missing images, uncertain page order and changes of writer before presenting a complete transcription.

## Read and check

Make an initial transcription of all assigned pages. Preserve actual spelling, abbreviations, unusual words, child language and incomplete sentences. Do not substitute familiar quotations or improve the author's prose. Follow the task's notation for unreadable spans.

For an uncertain word, consider a few possible readings. Compare them with the whole visible word: its length, beginning, ending, joins and position. Use the surrounding sentence to suggest possibilities, then return to the strokes. Reject a fluent reading if its letters do not fit. Keep an unknown span when the image does not support a choice.

Check the complete final lines against the image, including their beginnings and endings. Correct only differences supported by visible marks. Make one complete review, then use further inspection for specific unresolved spans or newly supplied evidence. Do not keep replacing words through repeated whole-text rereading merely because a different sentence sounds more plausible. Follow explicit task limits and state actual coverage.

## Use evidence without turning it into an answer

If a same-writer reference packet is supplied, compare relevant forms visually. Its labels may be wrong; check them against their own crops. Do not transfer a reference word into a target just because the author used it elsewhere. Without a packet, visible repetitions on the assigned pages may help. This skill does not automatically extract examples or fetch other documents.

Treat OCR outputs as candidates, not votes. Agreement and confidence do not establish a verified reading.

Keep user corrections separate from independent predictions and preserve their question marks. A correction to one phrase does not verify the rest of the page. In blind evaluation, do not read evaluator answers, previous errors or target corrections. Save initial and final readings, unresolved spans and actual inspection coverage; brief image-based change notes are enough. Do not expose private reasoning or claim unsupported certainty.

This skill authorizes no external uploads or paid calls. Test material and evaluator answers are for separate evaluation, not ordinary reading.
