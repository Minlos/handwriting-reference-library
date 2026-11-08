# Read handwriting with an LLM

Read a whole collection, compare the writer’s recurring letter shapes, then reread it. Keep uncertain words visible and check the final text against the actual scan. This is a reusable workflow for suitable LLM hosts, not a trained OCR model or an accuracy guarantee.

## Two independent skills

| Skill | What it does | Download |
|---|---|---|
| [Extract handwriting references](skills/extract-handwriting-references/SKILL.md) | Reads the permitted source collection and selects source-tied examples with provisional labels. It does not transcribe the target letters. | [ZIP · 10.8 MiB](downloads/extract-handwriting-references.zip) |
| [Read handwriting](skills/read-handwriting/SKILL.md) | Alternates contextual hypotheses with checks of actual words and complete lines. Works with or without a supplied reference packet. | [ZIP · 1.1 MiB](downloads/read-handwriting.zip) |

Each download has one `SKILL.md` at its root. Optional exercises, input images and evaluator-only answers live under `test-material/`. Load only the skill for normal work. Keep evaluator answers out of blind model input. Both are plain Markdown for suitable LLM hosts; neither requires GPT, Ollama or the other skill. These revised standalone skills have not yet been benchmarked.

The [letter experiment plan](evaluations/LETTERS-TWO-SKILLS.md) separates reading instructions, automatic references and extraction instructions. Its corrected target letters are not included in the public downloads. The packaged diary examples are known diagnostics, not new held-out evidence.

The earlier combined workflow remains at [SKILL.md](SKILL.md), with [HOST.md](HOST.md) for crops/files and the [older three-file download](downloads/handwriting-skill.zip). Historical experiments retain their original snapshots; do not attribute those scores to the new standalone skills. Ollama helpers are optional experiments and are not required.

## Find the right material

| I want to… | Read |
|---|---|
| Transcribe handwriting | [SKILL.md](SKILL.md) |
| Extract crops or maintain files | [HOST.md](HOST.md) |
| Test concrete failure modes | [Behavioral cases](tests/behavioral/README.md) |
| Compare models or skill/reference effects | [Evaluation handoff](handoffs/skill-reference-evaluation/README.md) |
| See results and limits | [Three-page comparison](evaluations/comparison.md), [six-page comparison](evaluations/six-page-skill-reference/README.md) |
| Understand dataset and helper files | [Repository guide](references/repository-guide.md) |

The repository also contains the family diary dataset, because the skill and its author examples were requested together. Sources, crops, transcripts and indexes are data; evaluations and handoffs are research records. They are not additional instructions to load into the model.

## What has been demonstrated?

On one three-page diary comparison, Sol with the skill **and earlier author examples** made 32 character errors, versus 55 for plain Sol (2.21% versus 3.80% CER; 41.8% fewer errors). This does not separate instructions from reference effects. On the six-page test, DeepSeek improved with references alone but not with the skill alone; Gemma regressed in that test. In a separate matched comparison on pages 4 and 6, reading instructions alone reduced Gemma’s character errors by 12.4%. These are small calibration experiments, not proof of a general improvement. New whole-collection and final-verification instructions have not yet been benchmarked.

## Data and permissions

The public diary is by **Блашкевич Надежда Никифровна**, from the Minlos family archive. Its photographs, text and annotations use [CC BY 4.0](LICENSE-DATA.md). This data license does not assign a license to the instructions or helper code. Other private manuscripts used during development are not included here. Project guidance is in English; manuscript text retains its original language.
