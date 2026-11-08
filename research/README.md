# Research and earlier tools

Start with [measured results](evaluations/comparison.md) or the [new two-skill letter test plan](evaluations/LETTERS-TWO-SKILLS.md). The new standalone skills have no model-test results yet.

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
