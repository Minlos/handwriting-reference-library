# Reading-skill components on three modern Russian development pages

The diagnostic asks which reading-skill instructions merit further testing after an observed loss on the nine-writer selection. It uses no references and does not test reference extraction. Astra reads the same writer035, writer040 and writer065 images in six isolated contexts, once per condition. These pages were selected for a prior failure, a prior benefit and a known label discrepancy; they are development data, not independent validation.

**The combined short instructions score better than the full skill here, but the experiment does not establish a harmful module.** Repeated rereading with visual checks is worse than visual checks alone in this single run; adding contextual candidates reverses that pattern. Initial readings also vary substantially. Repeated independent runs and equal actual inspection effort are needed to attribute a cause.

| Instructions | Initial reading edits / CER | Final reading edits / CER |
|---|---:|---:|
| Plain request | 1050 / 11.12% | 599 / 6.34% |
| Visual word and final-line checks | 1000 / 10.59% | 545 / 5.77% |
| Visual checks + contextual candidates | 1887 / 19.98% | 521 / 5.52% |
| Visual checks + repeated rereading | 1250 / 13.23% | 801 / 8.48% |
| Visual checks + candidates + repeated rereading | 962 / 10.19% | 542 / 5.74% |
| Full frozen reading skill | 1004 / 10.63% | 676 / 7.16% |
| Transkribus 148545, matched conventional baseline | — | 1388 / 14.70% |
| Rehand, unavailable; no complete matched result | — | Not scored |

Each cell sums character edits over the same 9,445 reading-normalized reference characters across all three pages. Reading normalization is NFC, casefold, Unicode punctuation removal and whitespace collapse. Literal scores over 9,880 characters are in [metrics.json](metrics.json). These are published-label disagreements, not independently audited visual error counts.

The control performs two recorded image inspections per page; the other variants perform three, within a common maximum of three. This tests instructions under a shared maximum budget, not an equal-effort causal comparison. Every run saves its initial transcription before reviewing the image and preserves it in [predictions](predictions/). The selection-visible pilot is explicitly excluded from the matched metrics and retained under `pilot-P0-selection-visible` for traceability. The Transkribus row reuses unchanged saved results from the nine-writer comparison for these exact three image hashes and labels, rescored over this subset only. Rehand has no complete output for this subset and is not ranked.

Exact prompt excerpts are in [prompts](prompts/); the full skill is frozen in `PFULL.txt`. V compares complete words and final lines to the image. C explicitly proposes a small set of candidates using shapes and context. R repeats whole-page checks until no supported change or the stated limit. P0 has no added module. There are no external OCR calls, target references or supplied target labels in any reader context.

An earlier visual audit shows why scores need checking: writer035's scan says «река начала течь темней», while the supplied label says «полней». Writer040 contains a Shakespeare quotation that some predictions replace with different wording and an incorrect author. Writer065 contains a clause that earlier plain Sol omitted and a skill run recovered. Such cases support preserving literal image checks, but do not prove that any one instruction causes or prevents them.

Run `python3 score.py` here to recompute all initial and final scores. [The reader manifest](reader-inputs.json) points to the already published original scans and records their hashes; [the protocol](protocol.json) records the budget and limits. Keep these selected pages for development and use new writers for final evaluation.
