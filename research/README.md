# Research and earlier tools

Start with [measured results](evaluations/comparison.md) or the [new two-skill letter test plan](evaluations/LETTERS-TWO-SKILLS.md). The standalone skills now have [separate pilot results](evaluations/two-standalone-skills/README.md).

- [evaluations/](evaluations/) — saved results, raw replies and frozen skill snapshots.
- [handoffs/](handoffs/) — reproducible experiment instructions and scoring.
- [tests/](tests/) and [tools/](tools/) — diagnostic cases, validation and scoring programs.
- [legacy-workflow/](legacy-workflow/) — the earlier combined skill and optional Ollama helpers.
- [repository guide](references/repository-guide.md) — detailed background.

Historical records may retain original root-relative path strings. Those files now resolve under `library/` for data and `research/` for experiments. Frozen input snapshots and their hashes are preserved. Original photographs and crop pixels are unchanged.

Run checks from the repository root:

```sh
python3 research/tools/verify_library.py
python3 -m unittest discover -s research/tests
python3 research/handoffs/skill-reference-evaluation/prepare_inputs.py --validate-only
```

## Every accuracy comparison includes conventional OCR/HTR baselines

All handwriting-recognition comparisons, including past reports, must include conventional OCR/HTR software alongside the LLM conditions. Audit and enrich historical comparisons where matching conventional baselines are missing. Use an easy-to-run OCR baseline such as Tesseract with the correct script/language data, plus a suitable handwriting-recognition configuration such as Kraken with an identified Cyrillic recognition model when available. Include Rehand as a separate external-service baseline when it is tested. A report containing only different LLMs or prompt/skill variants is incomplete.

Run baselines on the same frozen held-out images and transcription scope, with the same CER normalization, ambiguity exclusions and aggregation as the LLM runs. Report whole-page recognition separately from recognition using supplied line/word polygons. Record engine/model versions, model hashes, preprocessing and segmentation, raw outputs, failures, runtime, cost and setup effort. Choose settings on development material only; evaluation answers must not influence recognition or settings. Check script and handwriting suitability, and disclose when a baseline was designed for printed text. Do not substitute segmentation-only output for an OCR result.

Every comparison table includes the conventional baseline rows. If a required configuration cannot run, show it as **not run** with the concrete reason; never assign an invented score or silently omit it. Earlier results on a different image subset remain separate and are not relabeled as same-sample baselines.

Measured retrospective baselines: [Tesseract and EasyOCR on seven historical test panels](evaluations/conventional-baselines/README.md), with raw outputs and exact subset scores.
