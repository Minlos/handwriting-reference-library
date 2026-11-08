---
name: handwriting-reference-library
description: Read handwriting collections in cycles by provisionally transcribe all supplied material, compare evidence across the collection, use available OCR readings, and reread every page after supported revisions. Applies across LLM hosts; distinguish visual reading from text-only OCR review.
---

# Handwriting reference library

## Match the task to available capabilities

The host supplies images, permitted references and any file or OCR tools. A vision model can read supplied images without a particular product mode. A text-only model may coordinate OCR or review candidate text, but must identify that role and must not claim to have visually inspected handwriting it cannot see. If the required image evidence is missing, state what is missing rather than inventing a reading.

Creating crops, saving a library and checking coordinates require an executable host or tool-using agent. Do not claim those actions, a mode switch or a reference lookup unless they actually happened. Read [HOST.md](HOST.md) when extracting temporary crops or maintaining a library; do not inject the host manual into every transcription prompt.

## Read the collection in cycles

For a collection, make a provisional first reading of every supplied image before concentrating on individual difficult passages. Inventory letter pages, envelopes, postcards, blank sides and photographs. Record each image as read, partly read, or visually inspected without readable text, with a reason where needed. Preserve wording, spelling and uncertainty. Record likely page groupings and writer matches as hypotheses until supported. For a single image, use the same cycle within that image.

After the first full pass, compare the whole permitted collection. Use recurring names, addresses, dates, phrases, word endings, letter shapes and joins to identify useful reference regions. Keep different or uncertain writers distinct. Related letters can establish context, but target strokes must support each changed reading. Search all relevant pages for evidence instead of imposing a fixed crop count. Retrieve only the regions needed for each comparison; a large collection need not fit into one model request.

Use available OCR or other reading tools to propose alternatives and locate disagreements. Preserve their independent outputs and processing settings. Check suggestions against the image and same-writer examples. Tool agreement alone does not verify wording. If a requested tool is unavailable, record the access failure and continue with available evidence.

Reread every page after collecting new evidence, including passages initially considered clear. Record changed spans with the earlier reading, proposed reading, source regions or tool clues, and the visual basis for the change. Keep unsupported alternatives uncertain. Refresh the provisional references only from reviewed images, then repeat the whole-collection comparison and rereading cycle.

Complete at least a full provisional pass and a full rereading pass for an authorized collection task. Continue while a cycle yields supported changes or new human corrections provide relevant evidence. Stop after a complete pass yields no supported changes, or at an explicit time/cost limit or concrete access blocker. Report actual pass coverage and unresolved spans; do not call an inventory or a single-page reading a completed collection pass.

## Extract temporary references during comparison

Start from supplied scans when a saved library is absent. Clear words on the target page or other same-writer pages are eligible during ordinary transcription. Select examples for a particular uncertain letter, join or word and compare them directly with its pixels. A shared prefix does not establish a whole word. Preserve unusual language when supported by the strokes.

With image tools, crop complete examples from original pixels and inspect the crop boundaries before use. Re-crop clipped examples and discard blank or irrelevant regions. Keep source page, coordinates, rotation and proposed wording with each temporary example. Without cropping tools, compare visible regions in place and describe the actual capability used.

Automatically assigned labels remain provisional until human confirmation. Crops can stay in the current workspace or memory; save a reusable library only when requested. Preserve tentative and unread spans in the requested output notation. Profiles are source-tied hypotheses, and confusing references can be ignored. A prompt-only model can compare only images the host actually supplies. Reference extraction can also run independently using [the extraction skill](skills/extract-handwriting-references/SKILL.md).

## Treat OCR and confidence as evidence to check

An OCR result is a candidate, not ground truth. When the workflow includes OCR review, check candidate differences against the target pixels. Preserve unusual wording when supported; do not repair the text into plausible adult prose. Candidate agreement and model confidence do not verify a label. Keep the independent reading when the host asks for a before/after comparison.

### Verify the final text against the scan

Before presenting a transcription as visually checked, return to the image and check the complete final lines, including their beginnings and endings. Reading an image earlier, rereading the candidate text, or checking a PDF layout is not this pass. Do not silently carry an earlier guess into the final reading because the sentence sounds natural. Compare the whole word: approximate length, visible letters and joins, grammatical ending and position in the line. A familiar phrase cannot replace a differently written word.

For each disputed span, compare competing readings with the target strokes and useful same-writer examples. If neither is supported, retain an unknown span. Report exactly which lines remain partial or were not checked; a second pass is not evidence that the reading is correct. Revisit high-confidence phrases too, since plausible substitutions can survive an OCR/model consensus.

## Preserve confirmation boundaries

`verified` means wording explicitly confirmed or corrected by a human, with its source recorded. It does not certify every glyph or punctuation mark. `provisional` means a visually supported but unconfirmed reading. Keep unresolved alternatives separate. A correction to one fragment does not confirm the rest of its page.

After corrections, keep the supplied reading distinct from independently improved recognition. Return to related unresolved passages when relevant, and report only changes actually supported by images. Do not claim that reference growth itself improves accuracy or changes model weights.

Record human corrections verbatim with their page and source; preserve the person's question marks and alternatives. A supplied uncertain span remains uncertain. Update the working transcription before reusing it, and keep old predictions separate for evaluation. When a user identifies a page by its date or opening words, retrieve that page and show its complete current transcription inline, with unresolved spans marked.

## Evaluate and share without changing the evidence

For blind tests with references from other pages, keep reference pages separate from targets. Evaluate extraction from the target scan as a separate condition with no corrected target text. Do not supply corrected target text, overlapping target crops, error logs or target-derived profiles to a blind reading. Preserve failures and changed-prompt retries separately. Use the same images and generation/output settings when testing a condition change. Instructions, references and OCR can each help or hurt; no fixed accuracy is promised.

This is plain Markdown for any suitable LLM host. Optional local backend instructions are in [LOCAL.md](LOCAL.md) and [OLLAMA.md](OLLAMA.md). Model suggestions remain subject to visual and human review.

For maintainers, [behavioral cases](tests/behavioral/README.md) test concrete failure modes. They are known regression examples, not an untouched accuracy benchmark. Passing them does not establish general skill uplift.
