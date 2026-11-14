# OCR comparison requirements

- Include conventional OCR/HTR software in every recognition comparison; comparing only LLMs or skill/prompt variants is insufficient.
- Apply this retrospectively: audit and enrich all past comparisons whose matching conventional baselines are missing.
- Start with Tesseract (correct language data), EasyOCR or PaddleOCR (Cyrillic recognition), and a suitable Kraken/HTR configuration where available. Report Rehand separately as a service.
- Use identical held-out image bytes, transcription scope, normalization, exclusions and scoring populations. Full-page pipelines and supplied-region recognition are separate tests.
- Preserve existing raw outputs and historical protocols. Reuse baseline predictions only for identical inputs; rescore only with the exact comparison-specific evaluator/reference version.
- Record software/model versions, model hashes, segmentation and preprocessing, raw outputs, failures, runtime and cost. Choose settings on development data, not evaluator answers.
- Do not silently omit a baseline or invent a score. A missing/unsupported run is explicitly not run, with its reason; adding that placeholder alone does not complete the requested retrospective tests.
