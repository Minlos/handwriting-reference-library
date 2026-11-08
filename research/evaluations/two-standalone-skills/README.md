# Separate extraction and reading tests

This is a small calibration experiment on known project material, not evidence of a universal improvement. The reading skill and automatic reference extraction have different effects across readers and collections. Final frozen outputs supersede the earlier progress scores. Completed and failed attempts are both retained.

## What the results support

**Neither standalone skill has demonstrated a reliable general improvement.** The reading instructions help some readers/collections and hurt others. Automatically extracted references can also help or hurt. Verified source readings do not make the extraction instructions consistently better.

The strongest practical result is conditional: when raw reference packets are already supplied, the reading skill reduces errors for Sol, Astra and DeepSeek on both tested collections. Gemma worsens in both of its tested subsets. Grok improves on its one completed diary page, but its letter comparison is unavailable. These are single trials on small, previously inspected material; do not interpret this pattern as a guarantee.

The extraction instruction comparison is also mixed. On raw Popov sources, skill-built packets help downstream Sol, Astra and Gemma relative to ordinary extraction, but hurt DeepSeek. On raw diary sources, the packet helps Astra, DeepSeek, Gemma and Grok, but hurts Sol. These are effects of the **Sol-generated packets** on downstream readers, not direct measurements of every model as an extractor.

**The Popov pilot is particularly limited:** it scores 590 normalized reference characters from three resolved image excerpts, including a faint isolated line. It does not measure complete-letter accuracy. Cropping removes context and can change a reader's behavior. The diary panel contains 2,702 normalized reference characters across six pages. Never pool these two denominators or compare full-page and excerpt scores as equivalent.

Lower CER is better. Each cell is **baseline → comparison (matched targets)**. Diary targets are full pages; letter targets are selected resolved excerpts from three corrected letters, not whole-letter accuracy.

| Reader/setup | Collection | Reading skill, no references | Reading skill, same raw references | Extraction skill, raw sources | Extraction skill, verified sources |
|---|---|---:|---:|---:|---:|
| sol | diary | 3.03 → 3.44 (6) | 4.40 → 3.40 (6) | 2.07 → 3.40 (6) | 3.52 → 3.55 (6) |
| sol | letters | 18.47 → 16.61 (3) | 18.81 → 15.25 (3) | 16.27 → 15.25 (3) | — |
| astra | diary | 1.63 → 1.67 (6) | 2.37 → 1.85 (6) | 1.89 → 1.85 (6) | 1.55 → 1.81 (6) |
| astra | letters | 17.46 → 18.81 (3) | 14.07 → 13.90 (3) | 15.93 → 13.90 (3) | — |
| deepseek | diary | 20.98 → 17.36 (6) | 22.23 → 18.63 (5) | 20.32 → 19.39 (6) | 19.84 → 20.10 (6) |
| deepseek | letters | 37.63 → 42.37 (3) | 48.64 → 41.86 (3) | 36.61 → 41.86 (3) | — |
| gemma | diary | — | 33.63 → 35.07 (2) | 35.96 → 35.07 (2) | 60.16 → 37.40 (2) |
| gemma-letters-recovery | letters | 43.39 → 62.88 (3) | 58.64 → 68.64 (3) | 70.51 → 68.64 (3) | — |
| grok | diary | 6.40 → 7.28 (1) | 7.06 → 5.74 (1) | 9.27 → 5.74 (1) | 6.62 → 8.83 (1) |

## Concrete errors in the saved outputs

The L09 reference is **«Сейчас здоров, настроение ничего.»**, explicitly corrected by the contributor. The fixed task requests only the bottom complete line of this crop; adjacent partial ink is not part of the target.

- Sol without the reading skill: «Вашего здоровья и огромными силами».
- Sol with the reading skill: «Сейчас здоров и с прежним мином.» The opening improves, but the mood statement is still wrong.
- Astra without the skill: «Все же здоров и сравнительно [unclear].»
- DeepSeek without the skill: «Его Высокоблагородію милостивому государю». This is unrelated wording, not a supported reading.
- Gemma without the skill in the letter recovery: «в 14-м году в городе [unclear] в [unclear]».

These examples explain why plausible language and a claim of checking the image cannot establish accuracy. They also show why this short, low-contrast crop should not be used to judge whole-letter performance. The unchanged predictions and target image are available for inspection.

## What is isolated

A: neither skill nor packet. B: reading skill only. C: raw-source skill-built packet only. D: same packet plus reading skill. E: ordinary-extractor raw packet plus reading skill. Diary-only F/G use verified-source packets with/without extraction instructions respectively, with the same reading skill. Reading effects are A→B and C→D. Extraction effects are E→D and G→F.

The extractor in this pilot is Sol in fresh contexts; the table names the downstream reading model. This does not test Gemma/DeepSeek/Grok themselves as extractors. Both extractors receive the same source collection and six-example budget. The ordinary extractor receives a reasonable request, not a deliberately weak baseline.

Popov extraction sees only 27 raw sides of 14 other letters; no corrected Popov text is supplied to it. Diary extraction uses pages 4/6/7, either raw or accompanied by contributor-corrected source readings. Diary targets are pages 1/2/3/5/8/9. Letter targets are resolved image regions from 11.04.43, 22.01.44, 10.12.43.

## Scope and failures

Each agent condition has a fresh context without target corrections or other conditions. Separation is procedural, not an operating-system sandbox. All target scopes are fixed before scoring. One trial, different provider image handling and different model runtimes do not establish a general model ranking. Subagent runs may spend different amounts of effort; an additional time-matched control is still needed.

Raw extractors reported surveying every source image, not a complete line-by-line provisional read. The skill run therefore did not demonstrate its required full-reading cycle. All 36 saved reference crops reproduce their recorded supplied-image pixels exactly; that validates geometry, not label accuracy. Packets were frozen without post-score repairs.

Some reading agents did not complete the requested final recheck: Astra B and Sol G reported one image-reading pass only. These are actual workflow outcomes, not proof of compliant execution.

Gemma’s original 16,384-context run stopped after a timeout. Its completed diary subset is shown only where matching pairs exist; it has no baseline-only diary comparison. Gemma letter recovery uses a separate protocol (8,192 context, 1,024 output tokens) and is not pooled with that diary run. DeepSeek’s interrupted D01/C attempt is retained; its C→D diary comparison uses five common completed pages. Grok is a smaller command-line API pilot, not an installed Grok CLI or subscription UI. It completed the diary panel and part of the letter panel, then timed out on L01/D; no automatic retry was made. Its letter extraction comparison is unavailable, not zero error.

CER uses NFC, case/punctuation removal, collapsed whitespace and distinct ё/е. Placeholder letters such as unclear remain in scored output; no post-hoc error masks are added. Missing/failed conditions receive no score. Each pair uses the same completed targets and sums edits/reference characters. See [metrics.json](metrics.json) for exact counts, IDs and failure states.

## Evidence

Unchanged final [predictions](predictions/), [reference packets](reference-packets/), evaluator-only [gold](evaluator/gold.json), [target locations/hashes](targets.json), and [skill snapshots](skill-snapshots/). Evaluator gold must stay out of tested model contexts. No model is trained or fine-tuned.

## API progress and cost

- gemma: stopped_after_error; new recorded cost/estimate $0.000000.
- gemma-letters-recovery: finished; new recorded cost/estimate $0.000000.
- deepseek: finished; new recorded cost/estimate $0.054306.
- grok: stopped_after_error; new recorded cost/estimate $0.427424.

DeepSeek recorded cost includes a $0.02 reserve for an interrupted request. Old xAI reported spending $1.779612, old DeepSeek peak estimates $0.065310036, and old unreported xAI timeout reserve $0.25 are carried forward. New DeepSeek cap $0.15 plus new Grok cap $0.60 keep the maximum combined amount under the user’s $3 ceiling. Gemma runs locally. No keys are stored in this report.

Conservative combined spending, including estimates and timeout reserves, is **$2.657**, below the $3 ceiling. See [budget.json](budget.json). The new Grok timeout has an additional $0.08 reserve.

API prompts/image hashes and model metadata are in [provider records](provider-records/); [execution settings](execution-settings.json) distinguish the local recovery protocol. Subagent prompt constraints and coverage are summarized here; their full host execution traces are not exported as part of this test pack.

## How to interpret the metrics

CER is Levenshtein character edits divided by normalized human-reference characters. Insertions, deletions and substitutions all count; it can exceed 100% for a very wrong individual prediction. Aggregates sum edits and reference characters instead of averaging page percentages. The experiment uses the same normalization across its conditions: NFC, lower case, punctuation removal, collapsed whitespace and distinct ё/е. The letters in output placeholders such as `unclear` remain scored; this is stated explicitly because other historic protocols stripped such placeholders. Do not pool scores across protocols.

The main comparisons use the intersection of completed target IDs for the two conditions. The table shows the number of matched targets in each cell. A failed request is not a perfect score and does not silently disappear from the failure record. In particular, DeepSeek's reference-assisted reading comparison has five diary pages; its other diary comparisons have six. Gemma's original diary comparisons have two. Grok has one diary page and no complete matched letter comparison.

Relative error reduction, where needed, is `(baseline CER − comparison CER) / baseline CER`; negative values mean more errors. The exact edits, denominators, target IDs and relative reductions are in metrics.json. No significance claim or stable confidence interval is justified by this one-trial pilot.

## What was tested and what was not

Each source extractor was given the same collections and a limit of six examples per writer. Raw-mode labels remain provisional. In verified-diary mode, only wording supplied in the source readings can be treated as human-confirmed; the unresolved source word remains excluded. All packets were frozen before target scoring, and the ordinary and skill extractors never received corrected target text. Writers were not mixed.

The extraction experiment measures **downstream usefulness of a frozen packet**. It does not produce a complete gold-standard precision score for labels from the uncorrected Popov sources. The geometry check reproduces 36 real crops from supplied pixels, but a geometrically correct crop may have an incorrect label or be a poor example.

The reading experiment measures the outcome of supplying reading instructions to a particular host/model setup. Some agents performed more image checks than others, and some did not follow every instruction. The difference therefore includes actual workflow behavior and effort. It is not a clean estimate of wording alone at identical inference effort. No model weights were trained or changed.

## Next experiments warranted by these results

1. Score known regions while supplying the **whole Popov scans**, keeping uncertain reference text out of scoring. This tests whether the faint excerpt result survives when context is available.
2. Add newly corrected letters as a genuinely reserved evaluation set; keep source letters separate from targets and do not revise prompts after looking at target errors.
3. Repeat complete matched trials, including a time/call-matched extra-reading control. Preserve every failure and report variation rather than selecting the best attempt.
4. Evaluate the extraction skill with other extractor models as well as Sol. Audit proposed labels independently before claiming label accuracy; keep corrected-packet results separate from automatic-packet results.
5. Test coverage compliance explicitly: a full source reading, supported reference revision and a final complete-line image check must be recorded as actually performed. The current raw extraction runs do not establish that those cycles happened.

## Reproducing and checking

The public test folders contain actual Popov excerpt images, fixed scopes, source locations and evaluator-only answers. The extraction test folder lists the 27 permitted raw source URLs and hashes. The diary images and frozen original protocol remain in the library/research sections. Keep evaluator answers, previous predictions and other conditions out of the tested model context.

Use research/tools/report_two_skills.py on saved run data to regenerate paired scores without model calls. The reporting tests check that failed cases cannot change a pair's population, that missing conditions have no score, that source and target letters do not overlap, and that fixture image hashes/dimensions match their recorded bounds. All 21 repository checks pass. These checks validate the materials and scoring, not model accuracy.
