# Handwriting reference library: skill and diary dataset

**The skill and its reference data live together in this folder.** Clone or download this repository to get the model-independent reading instructions, optional test helpers, original diary photographs, labeled crops and indexes. No separate dataset download is needed.

Diary author: **Nadezhda Nikifrovna Blashkevich (Блашкевич Надежда Никифровна)**, the contributor's grandmother. Source: **Minlos family archive**, as reported by the contributor.

## Start here

1. Load [SKILL.md](SKILL.md) into an image-capable host. [HOST.md](HOST.md) describes file operations, OCR access and pass tracking.
2. Read every supplied image provisionally. Compare recurring handwriting across the whole relevant collection and use available OCR outputs as candidate readings.
3. Extract and inspect temporary examples, reread every page, record supported changes, and repeat until a full pass yields none. Preserve unresolved spans and human-confirmation boundaries.

A saved library is optional. The [standalone extraction skill](skills/extract-handwriting-references/SKILL.md) supports the same collection-wide comparison and rereading cycle. Recognition gains from this revised cycle remain to be measured.

The skill is a reusable workflow, not a trained OCR model. It can be used with other manuscripts too. The diary provides real reference examples for this author.

## Everything in this folder

| Path | Contents |
|---|---|
| [SKILL.md](SKILL.md) | The complete reading and reference-library workflow |
| [LOCAL.md](LOCAL.md), [local_read.py](local_read.py) | Optional local Gemma + GLM-OCR workflow |
| [OLLAMA.md](OLLAMA.md), [ollama_review.py](ollama_review.py) | Single-model review helper |
| [sources/](sources/) | 29 unchanged original JPEG photographs |
| [crops/verified/](crops/verified/), [verified.jsonl](verified.jsonl) | 56 user-confirmed word or phrase labels and crops |
| [crops/provisional/](crops/provisional/), [provisional.jsonl](provisional.jsonl) | 68 provisional visual readings and crops; review before treating them as ground truth |
| [index.csv](index.csv), [index.json](index.json) | All 124 crop labels, source coordinates, rotations and hashes |
| [transcripts/](transcripts/) | Working Russian transcripts for pages 1–9, with confirmation status and uncertainties |
| [source-manifest.json](source-manifest.json) | Original filenames, provenance, dimensions, rotation and hashes |
| [tools/verify_library.py](tools/verify_library.py) | Verify original hashes and exact crop reproduction; requires Pillow |
| [LICENSE-DATA.md](LICENSE-DATA.md) | CC BY 4.0 terms and attribution for the data |

## Experimental local tests

The local Ollama helpers are included for experimentation and comparison. They are not the recommended recognition setup: the tested Gemma configuration makes substantial reading errors, and the skill and reference pages do not reliably improve it. Select a model using measured accuracy on your own corrected pages.

[LOCAL.md](LOCAL.md) documents the optional Gemma + GLM-OCR test workflow.

Requirements: Python 3.9+, a running Ollama server and an installed model that accepts images. From this repository folder, replace `YOUR_VISION_MODEL` with that model's name:

```sh
python3 ollama_review.py --model YOUR_VISION_MODEL --image sources/IMG_20261031_190010425.jpg --library . --reference V001 --reference V013 --output ollama-suggestions/page-5.json
```

This reviews page 5 using two user-confirmed references from this same folder. It saves a new suggestion file and never changes the labels. Add `--dry-run` to check file loading without calling Ollama. For detailed letter comparisons, first make and visually inspect a correctly oriented crop. See [OLLAMA.md](OLLAMA.md) for the request format and limitations.

To validate the photographs and crops:

```sh
python3 tools/verify_library.py
```

## Cross-model evaluation handoff

Use the [separate four-condition handoff](handoffs/skill-reference-evaluation/README.md) to test skill and reference effects independently on another model or setup. It includes frozen inputs, blind-packet preparation, scoring and result templates. The current [skill revision](skill-revision.md) is vendor-neutral; older benchmark snapshots are preserved.

## Measured recognition results

See the [six-page four-condition comparison](evaluations/six-page-skill-reference/README.md) for Gemma, DeepSeek and OCR tests with the revised skill. The skill does not improve every model; reference pages can also cause regressions. [Other comparison results and reading examples](evaluations/comparison.md) use separate page sets. Fresh Sol tests cover pages 4, 6 and 7; the uncertain final word on page 6 is excluded. [Gemma comparisons](evaluations/gemma-pages-4-6-7/README.md) also cover all three pages. The [Gemma reference-crop test](evaluations/gemma-with-references/README.md) adds earlier-page author examples. The [Grok API test](evaluations/grok-three-example-pages/README.md) compares the same three example pages with and without the skill. Results from different page sets are kept distinct.

## Evidence and limits

The 56 confirmed and 68 provisional entries count crops, not individual words: some crops contain phrases or several lines. Rectangles can include neighboring ink; the label covers only the named phrase. Confirmation of wording does not certify every glyph or punctuation mark. Corrected comparison copies now cover pages 1–9; page 6 has one unresolved final word. Fragment-level confirmation sources remain separately recorded. See [review status](transcripts/review-status.json). Page 10 is still being reviewed. P11 is severely motion-blurred and has no labeled crop.

All pages have already been inspected during reference selection. This material supports handwriting comparison and calibration; it is not an independent recognition benchmark. Overlapping crops from a page must not be split between training and an independent test set. No untouched test pages have been reserved.

Coordinates are pixel edges in the original JPEG before rotation: top-left origin, x rightward, y downward, exclusive end boundaries. Reproduce a crop with `Image.open(source).crop((x0,y0,x1,y1)).rotate(rotation_ccw,expand=True)`. Source photographs are unchanged; no letters were reconstructed or generated. A mapping to earlier upload filenames has not been established.

Project descriptions and usage instructions are in English. Original diary text, labels and existing manuscript-specific reading notes remain in Russian.

## Data license and downloads

Photographs, diary text and annotations are available under **[CC BY 4.0](LICENSE-DATA.md)**. Credit the diary author and Minlos family archive, link to this project and the license, and indicate changes. The contributor confirmed authorization to publish and permit reuse, including commercial use; attribution and rights were not independently authenticated. This data license does not assign a license to the skill instructions or helper code.

The [release](https://github.com/Minlos/handwriting-reference-library/releases/latest) also provides a ZIP containing this same combined folder for users who prefer a download to a clone.
