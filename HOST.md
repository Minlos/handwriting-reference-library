# Host responsibilities for handwriting evidence

Load this document when extracting temporary references, creating or updating a reference library, or configuring a reading host. A single inference call needs the concise skill, target and permitted examples, not this operational manual.

## Supply capabilities honestly

The host loads images, selects references, prepares crops, calls models/OCR, saves artifacts and enforces category/write restrictions. An agent can perform these operations through real tools; a prompt-only model cannot. In ChatGPT, use an executable Work workspace for file operations when available. Other hosts may provide equivalent tools without that product mode. Image reading alone does not require a vendor-specific mode switch.

Keep authentication, model selection, local/cloud routing and budgets in host configuration. Follow the user's chosen provider and limits. Do not imply that a subscription includes paid API usage. Do not send credentials into model prompts or result files.

## Run whole-collection reading cycles

Maintain an image inventory and pass coverage. Read all supplied images provisionally before using the collection to revise difficult spans. Mark non-text sides and blocked images explicitly. Keep original first-pass transcripts and independent OCR results separate from later versions. Supply requested OCR services only through available, authorized access and budget settings; record unavailable tools and continue unaffected work.

Retrieve evidence across all relevant same-writer pages, crop complete source words, and inspect each resulting crop. Save source IDs, original-pixel bounds, rotation and proposed labels in the working record. Crop count follows the uncertainties being investigated. The model can receive selected regions in successive calls without receiving the whole collection at once.

After comparison, reread every image and record supported changes, regressions, unresolved spans and actual references consulted. Repeat while new visual support appears, within the user's limits. Stop after a full pass with no supported changes. New human corrections can trigger another full rereading cycle. A provisional label must never be promoted by repeated model agreement or by reuse in later passes.

During ordinary transcription, references may come from other regions of the target scan or other same-writer scans. Keep different writers distinct. Use only the permitted reference pages during restricted tests. Store working crops temporarily and export a reusable library only when requested.

## Save reproducible source evidence

Preserve original filenames, dimensions, orientation, hashes and provenance. Extract real raster crops; record page/region IDs, raw pixel coordinates, rotation, top-left origin and exclusive end bounds. Keep originals unchanged. Resized/enhanced viewing copies must be separate and have recorded transforms; do not generate or reconstruct handwriting strokes. Do not invent a mapping to earlier upload filenames.

View each crop and include full letters and marks. Rectangles may contain neighboring ink; the label applies only to its stated phrase. Record punctuation/editorial differences rather than silently normalizing wording. Verify exact source-pixel reproduction, paths, categories and hashes before packaging.

For a saved library, maintain crop PNGs, contact sheets, index.csv, index.json, source-manifest.json, a source-tied handwriting profile, unresolved records and a README. An error log contains known prior readings only. Keep confirmed, provisional and unresolved data separate. Grammar, familiar names and agreement between models cannot promote a label to verified; store the human confirmation source. Do not overwrite verified labels from an inference script.

## Make reference use configurable

Initialize or extend the library after corrections when library work is part of the task. During ordinary reading, avoid rebuilding or scanning the entire corpus unnecessarily. An agent may select a few permitted non-target crops; a prompt-only host supplies a fixed documented set. There is no measured universal optimum for reference count.

Do not automatically load a long profile into every prompt. Supply it only when explicitly enabled, with its provenance, scope and truncation recorded. Record actual reference IDs, labels and categories. If references are absent or unhelpful, permit reading from the target without inventing a comparison. Output examples and unclear candidates remain suggestions.

When corrections change a phrase boundary, recrop the whole phrase rather than treating it as an isolated letter change. Update the relevant profile/error history and inspect genuinely related ambiguities. Record changed readings, new support and unresolved items; no prior baseline means no independent before/after gain claim.

## Keep experiments reproducible

Freeze skill, reference set, target pixels, labels, masks, settings and output format before a run. Use fresh model contexts and expose only permitted inputs. Skill and reference access are independent conditions; the [evaluation handoff](handoffs/skill-reference-evaluation/README.md) defines the four-cell comparison. Keep OCR review or altered image presentation as separately named experiments.

Reserve truly new pages before library inspection when independent validation is intended. Existing inspected pages support calibration, not an untouched-test claim. A model told the corrected target text, including through a skill example, cannot later be called blind on it. User-approved comparison references and word-by-word independently verified labels are different evidence; record the acceptance basis.

Keep failures and recovery attempts, exact requests, source hashes, runtime/model versions, reported costs and scoring denominators. Never remove difficult known words merely because a model marks them uncertain. Apply only frozen, justified uncertain-span masks equally across conditions.

## Share only intended artifacts

Package the skill with the supporting files its host actually needs. Keep photographs separate unless the owner has authorized sharing them. Existing diary data in this repository have their documented license and confirmation limits. Do not claim that an updated skill has improved recognition before testing it. Preserve old evaluation snapshots when revising the current skill.
