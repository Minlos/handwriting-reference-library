# OCR comparison requirements

- Include conventional OCR/HTR software in every recognition comparison; comparing only LLMs or skill/prompt variants is insufficient.
- Apply this retrospectively: audit and enrich all past comparisons whose matching conventional baselines are missing.
- Start with Tesseract (correct language data), EasyOCR or PaddleOCR (Cyrillic recognition), and a suitable Kraken/HTR configuration where available. Report Rehand separately as a service.
- Use identical held-out image bytes, transcription scope, normalization, exclusions and scoring populations. Full-page pipelines and supplied-region recognition are separate tests.
- Preserve existing raw outputs and historical protocols. Reuse baseline predictions only for identical inputs; rescore only with the exact comparison-specific evaluator/reference version.
- Record software/model versions, model hashes, segmentation and preprocessing, raw outputs, failures, runtime and cost. Choose settings on development data, not evaluator answers.
- Do not silently omit a baseline or invent a score. A missing/unsupported run is explicitly not run, with its reason; adding that placeholder alone does not complete the requested retrospective tests.

## Select leaders on about 10 public pages, then use them routinely

- Run the initial system comparison on the same 9–12 public pages with supplied reference transcriptions for every candidate. Include ready OCR/HTR systems and Sol/Astra. Choose varied pages spanning relevant authors, document types, image quality and handwriting difficulty; report the limits of this selection sample.
- Every system must receive identical image bytes and be scored against the same frozen reference text (distinguishing supplied dataset labels from visually verified labels), transcription scope, ambiguity exclusions, CER normalization and aggregation. Whole-page and supplied-crop experiments are separate. Saved results from different image inputs cannot establish a winner.
- Maintain an explicit candidate inventory with completed and unresolved runs. Initial ready-system candidates: Tesseract, EasyOCR, Kraken, Russian CRNN, Rehand, PaddleOCR, Calamari and Transkribus. PaddleOCR and Calamari remain untested until actually run or a concrete incompatibility is documented. Require an applicable recognition checkpoint, not just installation. Rehand must participate because its small existing pilot is competitive, but that pilot does not establish a winner.
- Select the top performers from this matched public-page comparison using CER, failures and coverage, with runtime and cost reported. Show per-page results and paired uncertainty; disclose close or unstable rankings. Retain task-specific winners if diaries and letters differ. Do not claim general superiority from this small sample alone.
- Thereafter include the selected winners in every routine recognition comparison and retrospective update requiring matched baselines. Disregard losing ready-made systems in routine work; do not rerun them on every new page. Reopen selection only for a material new candidate, update or document type.
- Test other LLM systems specifically to understand the influence of the skill, using matched with/without-skill conditions. Separate reference effects from skill effects with matched with/without-reference conditions when applicable. These experiments do not require repeatedly benchmarking all discarded ready-made systems.
- Keep future evaluation material separate from these selection pages, freeze selected configurations, and prevent verified target answers from entering recognition prompts or reference extraction. Report selection-set results as selection results.
- Respect existing upload consent and spending limits. Blocked candidates remain explicitly untested. Do not claim the requested selection comparison complete while required runs remain unresolved.
