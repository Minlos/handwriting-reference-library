# Read handwriting with an LLM

Two independent, model-neutral skills. Open the files directly; no ZIP is needed.

| Start here | Purpose |
|---|---|
| **[Extract handwriting references](skills/extract-handwriting-references/README.md)** | Build source-tied handwriting examples from permitted scans, including uncorrected letters. |
| **[Read handwriting](skills/read-handwriting/README.md)** | Check contextual readings against actual letters and complete lines, with or without supplied examples. |

Each skill folder contains `README.md`, `SKILL.md` and optional `test-material/`. Only `SKILL.md` is needed for normal use. Test images are inside the test subfolder; evaluator answers must not enter a blind model context. Neither skill requires GPT, Ollama or the other skill. A small pilot now measures the standalone skills separately, with mixed results.

## Repository contents

- **[skills/](skills/README.md)** — the two skills and their separate tests.
- **[library/](library/README.md)** — original diary photographs, crops, transcriptions and annotations.
- **[research/](research/README.md)** — experiment results, evaluation plans, scripts and the earlier combined workflow.

## Evidence and tests

[Rehand scores on the Popov excerpts](research/evaluations/rehand-popov/README.md): **14.07% CER**, competitive in this small comparison, with different full-page versus cropped inputs.

One three-page Sol comparison with both instructions and earlier author examples produced 32 versus 55 character errors (2.21% versus 3.80% CER). This does not isolate the instruction effect. Gemma instructions alone reduced errors by 12.4% on two matched completed pages, but another six-page setup regressed. DeepSeek improved with references alone in that six-page test. These are small calibration experiments, not guaranteed gains or results for the new standalone skills. See the [results](research/evaluations/comparison.md).

See the [separate two-skill results](research/evaluations/two-standalone-skills/README.md) for the new comparisons.

The [Popov-letter pilot](research/evaluations/LETTERS-TWO-SKILLS.md) separates reading instructions, automatic references and extraction instructions. The private letter test collection is not included here. Public diary exercises are known diagnostics.

Diary data: Блашкевич Надежда Никифровна, Minlos family archive, [CC BY 4.0](library/LICENSE-DATA.md). That data license does not assign a license to skill instructions or helper code. Guidance is in English; manuscript text retains its original language.
