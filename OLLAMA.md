# Use the skill with Ollama

Use `SKILL.md` as instructions for a local image-reading workflow. The skill is model-independent. It is not a trained model, and copying it into Ollama does not give a text-only model image support or file tools.

In ChatGPT, the workflow always moves to Work mode. For Ollama, run the equivalent local workspace with original files and tools. There is no Ollama command that turns on ChatGPT Work mode.

## Review a crop locally

Requirements: Python 3.9 or newer, a running Ollama server, and an installed model that accepts images. Choose the installed model yourself; no model download is triggered by these files.

From this skill folder, replace `YOUR_VISION_MODEL`, paths, and reference IDs with values from your own library:

```sh
python3 ollama_review.py --model YOUR_VISION_MODEL --image /path/to/target.png --library /path/to/your-library --reference V004 --reference V013 --output /path/to/suggestions/review.json
```

This example sends the target crop plus two user-verified references to the local Ollama server. It reads `SKILL.md`, asks for visible evidence and unclear spans, and writes a new suggestion file. It does not edit the index or promote a label. It does not include the target's existing label in the request. The references help comparison; this is not an independent accuracy test.

Use `--dry-run` to validate image loading and request preparation without contacting Ollama. Use `--url` only if you intentionally want another Ollama endpoint. There are at most four reference images per request, because model limits and memory differ. The default endpoint is `http://localhost:11434/api/generate`.

For a new photograph, pass that image to `--image`. Crop it in the host program at its real coordinates before asking for detailed letter comparisons. Keep uncertain model output out of the labeled reference library until a person has reviewed the pixels.

## Build or update a whole library

An agent with image and file tools can load `SKILL.md` and carry out the full workflow. When using Ollama directly, a host program or a person must supply the source files, inspect proposed crop boxes, create crops, maintain the index, and check labels. The included review script assists image reading; it does not automatically transcribe or label the entire diary.

The request format follows Ollama's official [Generate API documentation](https://docs.ollama.com/api/generate): images are base64-encoded request fields, `stream: false` returns one response, and `format: json` requests JSON output.

Validation in this package: request preparation and a mocked API-response round trip were tested. A real local `gemma4:12b` image request also completed. Its reading conflicted with visible text and was rejected; recognition quality is not established. One run returned no complete answer before its output limit. The script marks empty or truncated output as incomplete. For a model that supports the `think` parameter, `--no-think` disables thinking; it does not improve or certify accuracy.

## Library format used by the helper

`--library` points to a folder containing `index.json`. The file has an `entries` list. Each referenced entry needs these fields:

```json
{
  "entries": [
    {
      "id": "V004",
      "category": "verified",
      "label": "the exact user-confirmed word or phrase",
      "crop_path": "crops/verified/V004.png",
      "crop_sha256": "the SHA-256 hash of the actual PNG file"
    }
  ]
}
```

This is a schema example, not a labeled manuscript sample. Replace the label, path, and hash with real evidence. Reference crop paths are relative to the library folder. The helper rejects a provisional reference, a path outside that folder, or a mismatched file hash. Without `--reference`, the target image can be reviewed without a library.

## Skill and data in the same folder

This repository includes the original diary photographs, index and crops beside `SKILL.md` and this helper. Run from the repository folder and pass `--library .`. For example:

```sh
python3 ollama_review.py --model YOUR_VISION_MODEL --image sources/IMG_20261031_190010425.jpg --library . --reference V001 --reference V013 --output ollama-suggestions/page-5.json --dry-run
```

Remove `--dry-run` to contact your local Ollama server. The data use [CC BY 4.0](LICENSE-DATA.md); see the [README](README.md) for author attribution and evidence limits. The release ZIP contains the same combined folder. For a different manuscript, supply its own originals and reference library instead.
