"""Build readable summaries from the saved metrics; never run recognition."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'metrics.json').read_text())
labels={('astra','A'):'Astra, no references',('astra','B'):'Astra, raw-scan references',('astra','C'):'Astra, source-text-assisted references',
        ('sol','A'):'Sol, no references',('sol','B'):'Sol, raw-scan references',('sol','C'):'Sol, source-text-assisted references',
        ('deepseek','A'):'DeepSeek Flash API, no references',('deepseek','B'):'DeepSeek Flash API, raw-scan references',('deepseek','C'):'DeepSeek Flash API, source-text-assisted references (retry)',
        ('transkribus','plain'):'Transkribus 148545, default automatic layout'}
table='| Configuration | Completed scans | Reading edits / CER | Literal edits / CER |\n|---|---:|---:|---:|\n'
for r in data['rows']:
    table+=f'| {labels[r["model"],r["condition"]]} | {r["pages_completed"]}/9 | {r["reading"]["edits"]} / {100*r["reading"]["cer"]:.2f}% | {r["literal"]["edits"]} / {100*r["literal"]["cer"]:.2f}% |\n'
table+='| Rehand, service timeout on first scan | 0/9 | Not scored | Not scored |\n'
text=f'''# Same-author references on nine modern Russian scans

The experiment asks whether automatically extracted handwriting examples help a model read different pages by the same writer. It compares examples collected from raw scans with examples collected using those scans and their published source text. Success means fewer character edits against the same held-out transcription.

**References improve Astra, and raw-scan references improve DeepSeek, while both packets worsen Sol in this run.** Astra with source-text-assisted examples has the lowest CER among completed configurations. This is evidence for continuing same-author reference testing, not a general claim that references help every model. The reading skill is absent from every condition in this table.

## Reference effects differ between models

{table}
Every completed row uses the entire same nine-page document: 5,742 reference characters after reading normalization or 5,938 after literal normalization. CER is character Levenshtein edits divided by reference characters, not an average of page percentages. Both modes apply NFC and collapse whitespace. Reading additionally casefolds and removes Unicode punctuation; ё remains distinct. Literal retains case and punctuation. Lower is better. These figures measure disagreement with supplied text, not a complete independent audit of visual reading errors.

Relative to each model's no-reference row, reading edits fall 20.3% with raw references and 32.8% with assisted references for Astra; they rise 15.5% and 15.9% for Sol. One run cannot separate instruction effects from model run variation.

DeepSeek's raw-reference reading edits fall 13.5% relative to its no-reference run. Its assisted-reference result falls 2.8%, but uses a replacement attempt after the first attempt failed. These are within-model comparisons; API and tool-using model hosts differ.

## One modern writer supplies both source and held-out documents

The source is [HWR200](https://huggingface.co/datasets/AntiplagiatCompany/HWR200), revision `366a882a2b8d043d437126d2878bd3812ec55a94`. Upstream directory `hw_dataset/16` attributes all selected scans to writer 016. This is dataset attribution, supported by a visual comparison of the pages, rather than independently established personal identity.

- Sources: all seven scans of `original16`, essays about cultural heritage and educating artists. [See the source pages](source-contact-sheet.jpg) and [source manifest](sources-only.json).
- Held-out targets: all nine scans of `fpr16`, essays about reason and emotion, including *War and Peace* and *Eugene Onegin*. The last scan has only three written lines. [See the target pages](target-contact-sheet.jpg) and [target manifest](targets-only.json).

No image hash is shared across the split. The supplied source and target texts share no exact eight-word sequence under the recorded word-token comparison. This does not exclude shorter common phrases or unknown model pretraining exposure. The source document was selected for having enough modern same-writer material and a separate transcribed target document, before this recognition run.

## Extraction uses all source pages and keeps uncertainty visible

Astra independently applied the same frozen `extract-handwriting-references` skill in two fresh contexts. Raw extraction received the seven source scans only. Assisted extraction received those same scans plus their entire published source transcription, without page or word alignment. Neither extractor received a target image or target text.

Each extractor surveyed all sources and could retain at most 24 original-pixel examples, with the same maximum contact-sheet dimensions. The raw packet retains 18 provisional examples; the assisted packet retains 22 dataset-assisted-provisional examples. Every retained crop was inspected and verified pixel for pixel against its original image at its recorded coordinates. Labels have no independent human confirmation.

[Raw reference contact sheet](extract-raw/labelledcontact-sheet.png) · [raw packet](extract-raw/packet.json) · [assisted contact sheet](extract-labeled/labelledcontact-sheet.png) · [assisted packet](extract-labeled/packet.json).

Readers receive only the selected crop packet for their condition, never the full source transcription. The comparison tests two complete extraction workflows: counts and selected examples differ, so their contrast does not isolate label quality while keeping crop selection fixed. These packets contain word and phrase examples; a separate letter-only condition has not been tested. Packet hashes in [packet validation](packet-validation.json) distinguish the exact inference packet from public metadata with relative paths.

## Fresh readers receive identical target bytes

Requested models are `gpt-6-astra` and `gpt-6-sol`. Each condition uses a fresh isolated agent, a common faithful-transcription request and a maximum of three target image inspections per page. The actual recorded inspection counts are retained in [predictions](predictions/). Reference inspections are additional and recorded separately. The source/test roles and scoring rule were frozen in [the protocol](protocol.json). Scores join page predictions in numeric order and compare the whole document, because upstream text has no page alignment. No target labels are sent to readers.

The reading skill is tested separately in [the component diagnostics](reading-skill-diagnostics/README.md). Its results are not part of the reference table above.

## DeepSeek uses the same scans and packets through its image API

DeepSeek receives the identical nine JPEG files and, where applicable, the same labelled reference contact sheet plus its provisional labels. The packets were extracted by Astra, not by DeepSeek; this tests use of fixed references. Requests use `deepseek-flash`, non-thinking mode, temperature 0, original image detail and a maximum of 8,192 output tokens. Each independent request receives all nine pages and returns page-labelled JSON. The API has no tool-driven zoom or additional inspection passes. Provider-side image preprocessing differs from the Astra/Sol hosts, so this compares tested setups rather than isolated model weights.

The first assisted-reference request repeated text until the output limit and receives no CER. One fresh attempt with unchanged settings completed; its score is explicitly labelled as a retry. Both responses remain in [deepseek-api/](deepseek-api/). No completed alternative was discarded to select a better score. All four attempts together cost at most $0.027 using conservative peak token prices, including the failure; actual off-peak billing may be lower. Exact usage, prompt/image hashes and settings are retained. [Official pricing](https://api-docs.deepseek.com/quick_start/pricing/) and [vision documentation](https://api-docs.deepseek.com/guides/vision/) describe the API capabilities and rates used.

## Image checks show real gains and remaining mistakes

- Target page 6 visibly says «непростителен». Plain Astra substitutes «недопустим»; the assisted-reference run reads «непростителен». The same assisted run changes visible «позволили» to «разрешили». Better aggregate CER therefore still includes unsupported substitutions. [Original page 6](targets/page06.jpg).
- Target page 1 visibly says «юную Наташу». Plain Sol reads this phrase correctly; raw-reference Sol substitutes «повесть Наташу». This is a real error, but the comparison does not establish which reference or instruction caused it. [Original page 1](targets/page01.jpg).

These are selected inspected examples, not a full manual label audit. No scoring labels or model outputs were corrected after recognition.

## The conventional baseline has an automatic-layout failure

Transkribus used public model 148545, “Russian generic handwritten and typed 1,” with quick-recognition defaults on the identical original JPEGs. All nine server-exported images match the reader inputs byte for byte. The first page is split into 124 `TextLine` elements; the TXT export consists largely of short, reordered fragments. The measured result includes this layout failure and recognition errors. It does not establish the accuracy of the recognition model with correct text-line segmentation, another model, or a manually corrected workflow. [Job and input verification](transkribus-status.json).

Rehand was retried on the first identical target and timed out before returning recognition text. It has no score or aggregate rank. The recorded failure is under [predictions/rehand/plain](predictions/rehand/plain/). No overall ready-system winner is selected from this incomplete comparison.

## Reproduce the scores without making new model calls

Run `python3 score.py` in this folder. It checks the saved input hashes and scores all ten completed configurations. `fetch.py` can recover the selected original scans from the pinned archive using [the download manifest](download-manifest.json). The raw Transkribus ZIP stays local because it includes account metadata; public predictions preserve its TXT transcription and content hashes without that metadata.

Dataset license declared upstream: Apache-2.0. Credit Ivan Potyashin, Mariam Kaprielova, Yury Chekhovich, Alexandr Kildyakov, Temirlan Seil, Evgeny Finogeev and Andrey Grabovoy, “HWR200: New open access dataset of handwritten texts images in Russian” (2023). Dataset images and text are separate from the skill license.

The main limits are one writer, two copied essay documents, one run per configuration, possibly imperfect supplied labels and unknown pretraining exposure. Nine scans are not nine independent writers. The next confirmation should repeat the same conditions and add modern writers while preserving each writer's source/test split.
'''
(ROOT/'README.md').write_text(text)

D=ROOT/'reading-skill-diagnostics'
d=json.loads((D/'metrics.json').read_text())
names={'P0':'Plain request','PV':'Visual word and final-line checks','PVC':'Visual checks + contextual candidates','PVR':'Visual checks + repeated rereading','PVCR':'Visual checks + candidates + repeated rereading','PFULL':'Full frozen reading skill'}
t='| Instructions | Initial reading edits / CER | Final reading edits / CER |\n|---|---:|---:|\n'
for r in d['results']:
    a=r['aggregate'];t+=f'| {names[r["variant"]]} | {a["initial"]["reading"]["edits"]} / {100*a["initial"]["reading"]["cer"]:.2f}% | {a["final"]["reading"]["edits"]} / {100*a["final"]["reading"]["cer"]:.2f}% |\n'
b=d['conventional_baseline']['aggregate']['reading']
t+=f'| Transkribus 148545, matched conventional baseline | — | {b["edits"]} / {100*b["cer"]:.2f}% |\n'
t+='| Rehand, unavailable; no complete matched result | — | Not scored |\n'
(D/'README.md').write_text(f'''# Reading-skill components on three modern Russian development pages

The diagnostic asks which reading-skill instructions merit further testing after an observed loss on the nine-writer selection. It uses no references and does not test reference extraction. Astra reads the same writer035, writer040 and writer065 images in six isolated contexts, once per condition. These pages were selected for a prior failure, a prior benefit and a known label discrepancy; they are development data, not independent validation.

**The combined short instructions score better than the full skill here, but the experiment does not establish a harmful module.** Repeated rereading with visual checks is worse than visual checks alone in this single run; adding contextual candidates reverses that pattern. Initial readings also vary substantially. Repeated independent runs and equal actual inspection effort are needed to attribute a cause.

{t}
Each cell sums character edits over the same 9,445 reading-normalized reference characters across all three pages. Reading normalization is NFC, casefold, Unicode punctuation removal and whitespace collapse. Literal scores over 9,880 characters are in [metrics.json](metrics.json). These are published-label disagreements, not independently audited visual error counts.

The control performs two recorded image inspections per page; the other variants perform three, within a common maximum of three. This tests instructions under a shared maximum budget, not an equal-effort causal comparison. Every run saves its initial transcription before reviewing the image and preserves it in [predictions](predictions/). The selection-visible pilot is explicitly excluded from the matched metrics and retained under `pilot-P0-selection-visible` for traceability. The Transkribus row reuses unchanged saved results from the nine-writer comparison for these exact three image hashes and labels, rescored over this subset only. Rehand has no complete output for this subset and is not ranked.

Exact prompt excerpts are in [prompts](prompts/); the full skill is frozen in `PFULL.txt`. V compares complete words and final lines to the image. C explicitly proposes a small set of candidates using shapes and context. R repeats whole-page checks until no supported change or the stated limit. P0 has no added module. There are no external OCR calls, target references or supplied target labels in any reader context.

An earlier visual audit shows why scores need checking: writer035's scan says «река начала течь темней», while the supplied label says «полней». Writer040 contains a Shakespeare quotation that some predictions replace with different wording and an incorrect author. Writer065 contains a clause that earlier plain Sol omitted and a skill run recovered. Such cases support preserving literal image checks, but do not prove that any one instruction causes or prevents them.

Run `python3 score.py` here to recompute all initial and final scores. [The reader manifest](reader-inputs.json) points to the already published original scans and records their hashes; [the protocol](protocol.json) records the budget and limits. Keep these selected pages for development and use new writers for final evaluation.
''')
print('Wrote same-author reference report and separate reading-skill diagnostics')
