# Optional fully local reading: Gemma + the skill + GLM-OCR

Gemma is the general image-reading LLM applying `SKILL.md`. GLM-OCR is its specialized OCR assistant. `local_read.py` is the host that reads files, prepares the image, calls the local models and saves results. It is a bounded three-stage workflow, not an autonomous agent that installs software, browses, trains or publishes. You can also load this skill into another local agent with equivalent tools.

After setup, reading does not require ChatGPT, API keys or an Internet connection. Model weights are not included in this repository.

## Setup

Install [Ollama](https://ollama.com/download), Python 3.10 or newer, and Pillow. From this repository folder:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install Pillow
ollama pull gemma4:12b
ollama pull glm-ocr
```

These explicit setup commands download software and models. On Windows, use `.venv\Scripts\python` in place of `.venv/bin/python`. Use an existing Python environment with Pillow if preferred. The runner never downloads models. Other downloaded vision-model names can be supplied with `--gemma-model` and `--glm-model`; those roles are configuration, not a guarantee that every model follows the same prompts well.

## Read locally

With Ollama running, from this folder:

```sh
.venv/bin/python local_read.py --image crops/provisional/P007_P05.png --library . --reference V001 --reference V013 --output-dir local-runs/page-5-example
```

Use a new output directory each time. Add `--dry-run` to validate the image, reference paths/hashes and request plan without contacting Ollama. The example uses a target and two different, user-confirmed reference crops from this same folder; it does not supply the target's label.

For your own image, replace `--image`. You can omit `--library` and references. To select a real region, add `--box X0 Y0 X1 Y1` in original-image pixels, with exclusive end coordinates. Add `--rotation 90`, `180` or `270` to rotate that region counter-clockwise. The prepared target is saved as a lossless PNG, with source hash, crop coordinates and rotation recorded. Prefer a correctly located line or phrase for detailed handwriting comparisons; automatic page segmentation is not part of this runner.

Up to four reference images can be supplied. They must match their saved hashes. Verified references are preferred. A visually clear provisional reference can be used with `--allow-provisional-references`, with its category retained. A crop identical to the target cannot also be a labeled reference. The local handwriting profile is loaded when present; at most its first 6,000 characters are supplied, with the scope recorded. This is library-assisted reading, not a blind benchmark.

## What happens

1. **Gemma + the skill:** reads the target image independently, with the selected references and profile context, before receiving an OCR candidate.
2. **GLM-OCR:** receives the same target pixels with its `Text Recognition:` prompt, without the skill, reference labels or Gemma's answer.
3. **Gemma review:** receives the target image, the skill, the references and both candidate readings. It proposes a reading, marks uncertain spans and describes image evidence. It must preserve unusual wording rather than silently repair grammar.

The independent Gemma pass makes it possible to compare the combined result with Gemma alone. Each request is stateless; the host does not pass a previous model's context except for the explicitly supplied candidate text in stage 3. Models run sequentially and are unloaded after each request to limit memory use.

The output folder contains `target.png`, `run.json` with all raw model responses and provenance, and `report.md` with the three readings. Every actual run remains **review_required**, even if the candidates agree. Truncated, invalid or failed replies are marked and do not become readings. A partial run is saved; a nonzero exit status means some stages did not produce valid output. Original files, reference indexes and verified labels are never updated by this runner.

## Fully offline operation

The runner permits only loopback Ollama base URLs, disables HTTP proxies and redirects, requires locally downloaded vision models, and rejects cloud tags and reported remote-model metadata. It makes no external tool calls. The Ollama daemon is a separate application: for a strict local-only session, disable its cloud features too. With models already downloaded, one option is a separate server in a terminal:

```sh
OLLAMA_NO_CLOUD=1 OLLAMA_HOST=127.0.0.1:11435 ollama serve
```

Then add `--endpoint http://127.0.0.1:11435` to the reading command. This leaves an existing Ollama server on port 11434 alone. After downloading dependencies and models, you can disconnect the Internet and run against local files. See [Ollama's local-only guidance](https://docs.ollama.com/faq#how-do-i-disable-ollama-cloud).

The older `ollama_review.py` helper is a separate single-model tool and allows an explicitly configured endpoint; use `local_read.py` for this loopback-only workflow.

## Does combining models improve accuracy?

It might; this is a hypothesis to measure. OCR can supply plausible characters, while a general vision LLM can compare handwriting examples and flag disagreements. It can also introduce fluent but incorrect corrections. Model agreement is not verified evidence.

Compare all three outputs on the same correctly labeled line images. Report CER, the number of examples and reference characters, failures, and how much text was left uncertain. Keep target answers out of prompts and evaluation pages out of training/reference examples. Never merge uncertain or model-generated text into training labels automatically. A claim such as 95% character accuracy needs measured CER at or below 5% on held-out pages, not a few familiar samples.

This workflow is inference, not fine-tuning. It does not update Gemma or GLM-OCR weights. Fine-tuning and compatible model export are separate steps.

API reference: [Ollama generate endpoint](https://docs.ollama.com/api/generate). Check the skill and these files from the same version when sharing.

## Validation in this version

Ten automated checks cover loopback URL restrictions, remote-model rejection, exact target pixels across all stages, raw-coordinate crop/rotation reproduction, reference hashes and categories, target/reference identity rejection, no output overwrite, no calls during dry runs, and incomplete model output.

A real local run used the downloaded `gemma4:12b` and `glm-ocr:latest`, target P007 on page 5 and verified references V001 and V013. All three stages completed. GLM-OCR returned «Бадумисина малина»; Gemma independently read «Бабушкина мама» and retained it after review, matching the visible phrase on inspection. P007 remains a provisional library label, not a newly user-confirmed one. This is one functional example with reference context: it demonstrates rejection of an OCR error, not an accuracy gain over Gemma alone, a corpus benchmark, or evidence of 95% accuracy.
