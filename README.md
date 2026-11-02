# Handwriting reference library: skill and diary dataset

**The skill and its reference data live together in this folder.** Clone or download this repository to get the reading instructions, Ollama helper, original diary photographs, labeled crops and indexes. No separate dataset download is needed.

Diary author: **Nadezhda Nikifrovna Blashkevich (Блашкевич Надежда Никифровна)**, the contributor's grandmother. Source: **Minlos family archive**, as reported by the contributor.

## Optional fully local reading

Use **Gemma as the general image-reading LLM applying the skill**, with **GLM-OCR as a specialized OCR assistant**, through your local Ollama server. The included [local_read.py](local_read.py) saves both independent readings and a combined image-grounded review, without modifying verified labels. No ChatGPT session is needed for that run. See **[LOCAL.md](LOCAL.md)** for installation, offline operation and the three-output comparison.

## Start here

1. Load [SKILL.md](SKILL.md) into an agent with image and file tools. In ChatGPT use Work mode; for Ollama use a local workspace with access to the files. Ollama itself has no ChatGPT mode switch.
2. Read [handwriting-profile.md](handwriting-profile.md) and [index.json](index.json). Begin with user-confirmed examples, compare visible letter forms and return to the original photograph when uncertain.
3. Save proposed readings separately. Preserve uncertainties and the distinction between confirmed and provisional labels.

The skill is a reusable workflow, not a trained OCR model. It can be used with other manuscripts too. The diary provides real reference examples for this author.

## Everything in this folder

| Path | Contents |
|---|---|
| [SKILL.md](SKILL.md) | The complete reading and reference-library workflow |
| [LOCAL.md](LOCAL.md), [local_read.py](local_read.py) | Optional local Gemma + GLM-OCR workflow |
| [OLLAMA.md](OLLAMA.md), [ollama_review.py](ollama_review.py) | Single-model review helper |
| [sources/](sources/) | 29 unchanged original JPEG photographs |
| [crops/verified/](crops/verified/), [verified.jsonl](verified.jsonl) | 48 user-confirmed word or phrase labels and crops |
| [crops/provisional/](crops/provisional/), [provisional.jsonl](provisional.jsonl) | 68 provisional visual readings and crops; review before treating them as ground truth |
| [index.csv](index.csv), [index.json](index.json) | All 116 crop labels, source coordinates, rotations and hashes |
| [transcripts/](transcripts/) | Working Russian transcripts for pages 1–8, with confirmation status and uncertainties |
| [source-manifest.json](source-manifest.json) | Original filenames, provenance, dimensions, rotation and hashes |
| [tools/verify_library.py](tools/verify_library.py) | Verify original hashes and exact crop reproduction; requires Pillow |
| [LICENSE-DATA.md](LICENSE-DATA.md) | CC BY 4.0 terms and attribution for the data |

## Use with Ollama

Requirements: Python 3.9+, a running Ollama server and an installed model that accepts images. From this repository folder, replace `YOUR_VISION_MODEL` with that model's name:

```sh
python3 ollama_review.py --model YOUR_VISION_MODEL --image sources/IMG_20261031_190010425.jpg --library . --reference V001 --reference V013 --output ollama-suggestions/page-5.json
```

This reviews page 5 using two user-confirmed references from this same folder. It saves a new suggestion file and never changes the labels. Add `--dry-run` to check file loading without calling Ollama. For detailed letter comparisons, first make and visually inspect a correctly oriented crop. See [OLLAMA.md](OLLAMA.md) for the request format and limitations.

To validate the photographs and crops:

```sh
python3 tools/verify_library.py
```

## Measured recognition results

See the [single comparison table and reading examples](evaluations/comparison.md). Fresh Sol tests cover pages 4, 6 and 7; the uncertain final word on page 6 is excluded. [Gemma comparisons](evaluations/gemma-pages-4-6-7/README.md) also cover all three pages. Results from different page sets are kept distinct.

## Evidence and limits

The 48 confirmed and 68 provisional entries count crops, not individual words: some crops contain phrases or several lines. Rectangles can include neighboring ink; the label covers only the named phrase. Confirmation of wording does not certify every glyph or punctuation mark. Pages 4 and 7 have user-confirmed wording; page 6 has one unresolved final word. Other transcripts remain partly verified or provisional. P11 is severely motion-blurred and has no labeled crop.

All pages have already been inspected during reference selection. This material supports handwriting comparison and calibration; it is not an independent recognition benchmark. Overlapping crops from a page must not be split between training and an independent test set. No untouched test pages have been reserved.

Coordinates are pixel edges in the original JPEG before rotation: top-left origin, x rightward, y downward, exclusive end boundaries. Reproduce a crop with `Image.open(source).crop((x0,y0,x1,y1)).rotate(rotation_ccw,expand=True)`. Source photographs are unchanged; no letters were reconstructed or generated. A mapping to earlier upload filenames has not been established.

Project descriptions and usage instructions are in English. Original diary text, labels and existing manuscript-specific reading notes remain in Russian.

## Data license and downloads

Photographs, diary text and annotations are available under **[CC BY 4.0](LICENSE-DATA.md)**. Credit the diary author and Minlos family archive, link to this project and the license, and indicate changes. The contributor confirmed authorization to publish and permit reuse, including commercial use; attribution and rights were not independently authenticated. This data license does not assign a license to the skill instructions or helper code.

The [release](https://github.com/Minlos/handwriting-reference-library/releases/latest) also provides a ZIP containing this same combined folder for users who prefer a download to a clone.
