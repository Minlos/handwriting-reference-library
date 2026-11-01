---
name: handwriting-reference-library
description: Read handwritten diary pages and build an image-based reference library from user corrections and clearly legible words. Use for careful manuscript transcription, author-specific letter comparisons, and labeled crop libraries.
---

# Handwriting reference library

## Always use Work mode

This workflow does not work in ordinary chat alone. In ChatGPT, always switch to Work mode before inspecting files, making crops, or claiming to save a library. Carry over the original images, user corrections, and unresolved passages. Use an available mode-switch or handoff tool. If no such tool exists, explicitly ask the user to open Work mode; never claim that a switch occurred.

In Ollama or another local environment, Work mode means the equivalent executable workspace: access to original image files, a model that accepts images, and a host program or agent that can crop, save, and validate files. Ollama itself has no ChatGPT Work-mode switch. Use the local workspace instead. A text-only conversation or a pasted transcription is insufficient. Stop image-dependent work when the original images or required tools are unavailable, and state exactly what is missing.

## Optional fully local Gemma + GLM-OCR workflow

When the user chooses local execution, use a local image-capable general LLM (for example Gemma) to apply this skill and a specialized OCR model (for example GLM-OCR) as a source of candidate text. The host program supplies files, source coordinates, reference images and the local model calls. A model reading this file cannot itself execute tools or update files without that host.

Read [LOCAL.md](LOCAL.md) for the runnable `local_read.py` workflow. It saves an independent Gemma reading, a GLM-OCR reading and Gemma's image-grounded review as three separate results. Supply the same source pixels to each stage; preserve raw outputs and uncertainty. Gemma should compare the image and relevant reference crops rather than merely rewrite OCR into plausible prose. Reference categories remain visible; provisional examples require explicit opt-in and remain provisional.

Local execution is optional, with no ChatGPT dependency for the reading run. Preinstall the chosen models. Use loopback endpoints and downloaded local models; do not fall back to cloud models or pull weights silently. Follow the offline setup in LOCAL.md when the Ollama server must have cloud features disabled. Save suggestions into a new output directory, never over the originals or verified library.

Combining models is an experiment, not evidence of higher accuracy. Compare OCR alone, Gemma with the skill alone, and the combined review on the same examples. For accuracy evaluation, keep target labels out of prompts, avoid using the target as a labeled reference, and separate whole training/reference pages from evaluation pages. Agreement never promotes a reading to verified, and no fixed accuracy such as 95% may be promised without measured results on held-out pages. Training or fine-tuning is a separate task; adding the skill or references does not update model weights.

## Begin with clear words and one author's letter patterns

1. Inspect the clearest words first. Establish visible letter shapes and connections from those words before tackling difficult passages. Do not start by guessing unclear sentences.
2. Group pages by author only when supported by the user or evidence. Treat the supplied diary pages as one author's writing when the user confirms that fact. Keep other authors separate.
3. Prefer user-confirmed words. Compare repeated letters and connections across those words, then across the available pages. A matching shape is evidence to inspect; it is not automatic confirmation of a word.
4. Record the exact crop IDs supporting every pattern. Describe what is visible: loops, descenders, separate marks, joins, or variants. Do not invent a glyph rule from a corrected label alone.
5. Preserve word context. Do not label isolated characters when connected strokes make their boundaries ambiguous. Prefer a reliable word or phrase crop to a false character boundary.

## Consult the saved library before each new reading

Load `index.json` and `handwriting-profile.md` before reading a new page. For an uncertain word or letter group, retrieve the most relevant user-verified word/phrase crops and actually view them beside the target image. Record the reference IDs and what part is being compared. A shared prefix does not establish the rest of a word. Use provisional examples only with their category visible. If the library has no useful verified comparison, say so and leave the target uncertain. Reading the skill instructions or having a ZIP on disk is not evidence that the reference images were consulted.

After user corrections, retrieve the corrected crop and the related existing examples again. Distinguish a reading supplied by the user from one independently improved through comparison. Do not claim that examples were used before a correction if they were added afterward.

## Initialize after the first corrected page

Immediately after the user corrects the first page, and before transcribing the next page, build the first saved reference library. Inspect all available pages for clear additional examples. User instructions can change the sequence, but not the need for source evidence.

Maintain two separate categories:

- `verified`: labels explicitly confirmed or corrected by the user. Record the correction's source. User confirmation of wording does not prove that every glyph is visually clear.
- `provisional`: only words or phrases whose complete spelling is visually clear to the reviewer. Record that this is an uncalibrated visual judgment, not user confirmation.

Keep ambiguous candidates in a separate unresolved record with an empty label or explicitly tentative alternatives. Never add them as labeled reference examples just because they fit grammar, a familiar name, another model's output, or a verified pattern elsewhere. Another model agreeing does not make a label verified.

## Save real evidence

- Preserve original filenames, dimensions, orientation, file hashes, and source provenance. Never invent a mapping between renamed photographs and old uploads.
- Extract actual pixel crops from the original raster. Record page ID, region or line location, raw pixel coordinates, and any rotation. Specify the origin and whether end coordinates are exclusive.
- Keep source images unchanged. Rotation by quarter turns is allowed for reading. Keep enhanced or resized viewing copies separate from original crops. Never reconstruct letters or generate replacement manuscript images.
- For multi-line or sloping phrases, record that a rectangular crop contains nearby ink. Do not pretend that neighboring fragments belong to the label. Preserve user wording and record punctuation, capitalization, or spelling differences rather than silently normalizing them.
- Save crop PNGs, contact sheets, `index.csv`, `index.json`, `source-manifest.json`, `handwriting-profile.md`, an unresolved record, and `README.md`. Include an error log only for known prior errors; leave unknown prior readings blank.
- View every crop at useful size and verify that full letters and their marks are included. Check raw-coordinate reproduction against the original pixels. Check every index path, category, and hash before packaging the ZIP.
- Never claim that a library or profile was updated unless those files were actually created and verified.

## Apply the library to the reading task

When the user asks to improve a reading, the library is an intermediate result. Continue directly to the original unresolved passages, compare them against the saved examples, and produce the best supported transcript with uncertainties and source crops. Do not stop after packaging the library and wait for another instruction to start reading. Do not claim improvement merely because the library grew; show the newly readable text and what remains unresolved.

## After each correction

Add the new confirmed crop, update the profile and error record, inspect similar forms throughout the available corpus, and revisit earlier unresolved passages. If a correction changes word boundaries or several adjacent words, re-check and crop the entire phrase; do not treat it as a single-letter substitution. Report only readings that actually improved; leave unresolved ones unresolved. Do not promote a candidate merely because it resembles an existing crop. Preserve evidence and previous decisions when changing a label.

For accuracy testing, reserve separate pages before examining them for reference selection. Pages used to build this library are not an independent test set.

## Sharing and Ollama

This file is plain UTF-8 Markdown and does not require a particular vendor or model. An agent that supports skills can load this folder; otherwise provide these instructions to the model and run the file operations through the host program. See `OLLAMA.md` for the included review script. Model responses are suggestions requiring visual review, and the script must never overwrite verified labels.

Share this skill folder separately from private diary photographs unless the owner also intends to share the photographs. A skill is instructions, not model training or a guarantee of accurate recognition.
