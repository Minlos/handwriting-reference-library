# Read handwriting with an LLM

Read a whole collection, compare the writer’s recurring letter shapes, then reread it. Keep uncertain words visible and check the final text against the actual scan. This is a reusable workflow for suitable LLM hosts, not a trained OCR model or an accuracy guarantee.

## Use the skill

**Start with [SKILL.md](SKILL.md).** It contains the reading instructions. Load only this file initially. Read [HOST.md](HOST.md) when the task needs crops, files or OCR tools. You do not need the experiment archive or the diary dataset to use the workflow on your own scans.

The [small skill download](downloads/handwriting-skill.zip) contains these two files and a short entry guide — three files total. The [optional extraction skill](skills/extract-handwriting-references/SKILL.md) can also be used independently. Ollama helpers are optional experiments; they are not required and did not perform well on this diary.

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

On one three-page diary comparison, Sol with the skill **and earlier author examples** made 32 character errors, versus 55 for plain Sol (2.21% versus 3.80% CER; 41.8% fewer errors). This does not separate instructions from reference effects. On the six-page test, DeepSeek improved with references alone but not with the skill alone; Gemma regressed. These are small calibration experiments, not proof of a general improvement. New whole-collection and final-verification instructions have not yet been benchmarked.

## Data and permissions

The public diary is by **Блашкевич Надежда Никифровна**, from the Minlos family archive. Its photographs, text and annotations use [CC BY 4.0](LICENSE-DATA.md). This data license does not assign a license to the instructions or helper code. Other private manuscripts used during development are not included here. Project guidance is in English; manuscript text retains its original language.
