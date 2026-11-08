# Handoff: separate the effects of the skill and author references

Run the same four conditions on an image-capable LLM or host of your choice. This measures whether instructions help, whether references help, and whether their combination helps. The handoff is vendor-neutral; it makes no new accuracy claim.

| Condition | Skill snapshot | Author references |
|---|---|---|
| A | No | No |
| B | Yes | No |
| C | No | Yes |
| D | Yes | Yes |

The fixed reference pages are **4, 6 and 7**. The target pages are **1, 2, 3, 5, 8 and 9**. Each target is evaluated once in every condition: **24 primary readings per model and trial**. No reference page is a target in this protocol. Page 10 is still a correction draft and is excluded. All current material was previously inspected, so this is calibration rather than an untouched independent test.

## Start with the frozen inputs

Clone/download this whole repository, including sources/. Read [protocol.json](protocol.json), [base-prompt.txt](base-prompt.txt), [skill-snapshot.md](skill-snapshot.md), and [reference-labels.json](reference-labels.json). The snapshot and its hash identify this experiment; it does not silently follow later edits to the root SKILL.md. Source photographs remain unchanged.

The reference texts are corrected comparison copies, with editorial punctuation. Page 6's final word remains explicitly unresolved and is not a verified label. Pages 1–3 and 5 were rechecked in full and the user resolved 26/II-47 and «или 3 маленьких». The user corrected pages 8–9 and authorized their comparison use. Exact fragment confirmations remain in the library; reviewed comparison text is not independent certification of every glyph.

Use Python 3.10+ with Pillow to validate and export:

```sh
python3 research/handoffs/skill-reference-evaluation/prepare_inputs.py --validate-only
python3 research/handoffs/skill-reference-evaluation/prepare_inputs.py --output /path/to/NEW_BLIND_PACKETS
```

No network requests or model calls occur. The exporter verifies source and snapshot hashes, reproduces native target pixels and makes separate folders for each condition/page. Each contains task.txt, packet.json, the target image, and only its allowed skill/reference files. C/D include the same three 1800×2400 JPEG reference images and corrected reference texts. B/D include identical skill text. No gold, error log, author profile or target-derived examples are exported.

**Give the tested model only one packet folder per fresh context.** The coordinator may read this repository and gold/; the tested model must not inherit the coordinator conversation, repository access or other packets. Folder separation alone is not an operating-system sandbox. Record any practical isolation limit.

## Run without changing the question between conditions

Use one image-capable model version, image processing policy, generation settings, output format and permitted tool set across all four conditions in a trial. Supply the images as images, not filenames that the host cannot open. For a web chat, attach only the packet's files; for an API, encode the indicated images and include the permitted text; for a CLI/agent, use a clean workspace exposing only that packet. The model must actually receive the reference images in C/D. Merely attaching labels or installing a skill is not equivalent.

Inspect inherited system rules, auto-loaded skills, memories and search/tool access. A supposedly “without skill” condition must not receive it through a global installation. Preserve normal security controls; do not use unrestricted permissions to achieve isolation. If an interface cannot supply the required images or isolate context, mark the setup unsupported or clearly label it a different protocol. A text-only OCR reviewer is a separate workflow.

Keep the base prompt identical and add only the assigned factors. The generic prompt already asks for faithful Russian transcription and preserves unusual child forms; do not weaken A to manufacture uplift. Do not paste corrected target text, access gold files, search the public diary, select references using target answers, or use other target crops as references.

Counterbalance condition order across pages; for example A/B/C/D, B/C/D/A, C/D/A/B, D/A/B/C. Save exact requests, image hashes, snapshot hash, model/runtime identifiers, visible mode/settings, output limits, raw replies, completion status, usage, elapsed time and reported cost. Record unavailable settings as unavailable. Do not assume that subscription access includes API credits. Preparation authorizes no paid calls; use the operator's current budget and carry forward earlier spend rather than resetting it per process. Keep credentials outside prompts, results and Git.

Run one complete trial first. Repeated trials can estimate sampling variability, but require a separate cost/time decision; do not launch them automatically. No silent retries. Preserve the first failed or truncated response and put any changed-prompt recovery in a separate run/profile. Do not rerun only the worse conditions and then pool the best attempts.

## Record and score every primary attempt

Copy [results-template.jsonl](results-template.jsonl) and fill the setup, exact model, trial and each result. Use status `completed` with the actual transcription, or a truthful failure status such as `error`, `truncated`, `refusal` or `unsupported`. Preserve raw outputs separately. An `[unclear]` marker on known text is an attempted omission and stays in the scoring denominator; it is not an excuse to drop difficult words.

The evaluator-only gold/ files and hashes are frozen in protocol.json. The default six targets have no unresolved scoring masks. The unresolved page-6 word is in the *reference* material, not a target here. If a future protocol includes page 6 as a target, inspect its emitted unknown-word suffix and provide exact justified masks with the setup/model/trial/condition/page key; retain all known preceding text. Never edit gold or mask extra model errors after seeing scores.

```sh
python3 research/handoffs/skill-reference-evaluation/score_results.py --predictions /path/to/results.jsonl --output /path/to/NEW_metrics.json
```

Reading CER uses NFC, collapsed whitespace, case folding and removal of Unicode punctuation; ё remains different from е. Literal CER retains case/punctuation. Word error counts are also saved per page. Aggregate by **summing edits and reference characters**, not averaging percentages. A condition gets a complete-set CER only when all six pages completed; failures and missing pages remain visible. Do not rank successful-only scores from different page subsets as if coverage matched.

For complete matching conditions, report relative error reduction `(baseline CER − comparison CER) / baseline CER`:

- skill without references: A → B;
- skill given references: C → D;
- references without skill: A → C;
- references given skill: B → D;
- joint workflow change: A → D, explicitly not “skill alone”.

Negative values mean more errors. A zero baseline makes the relative reduction undefined. Show raw counts and failures, not just percentages. With a few calibration pages and one trial, small differences do not establish stable improvement.

## Return one comparable result table

Include A–D, per-page/aggregate CER, completion coverage, trial count, source/snapshot identifiers, actual setup differences and cost. Give concrete corrected-vs-misread examples, including regressions. Separate evidence from hypotheses. OCR-alone, OCR review, reference-selection methods or contact-sheet variants are separate experiments; do not silently mix them into these four cells.

Older [published results](../../evaluations/comparison.md) are context, not completed cells for this protocol: target sets, reference presentations, output formats and skill versions differ. Do not fill missing cells with historical numbers. Freeze a new protocol version before adding approved pages or revised instructions; never rewrite old benchmark snapshots. No further human transcription is required to prepare this handoff, and no new paid run is implied by opening it.
