# Handwriting reference library skill

A portable skill for reading handwritten pages and building an author's reference library from real image crops. User-confirmed labels stay separate from provisional visual readings. Unclear words remain marked rather than guessed.

The workflow starts with clear words, compares their letter shapes across the available pages, then returns to difficult passages. A library is an intermediate step when the task includes improving a transcription.

## Use the skill

- In an agent that supports skills, load this folder's `SKILL.md` or copy the folder into that agent's supported skill directory.
- In ChatGPT, use Work mode with the original images and file tools. If an automatic switch is unavailable, open Work mode manually. The instructions do not themselves add a mode-switch tool.
- With Ollama, use an image-capable model and a local host program or agent that can read, crop, save, and validate files. Ollama has no ChatGPT Work-mode switch.

Provide the original images, any user-confirmed corrections, and the desired output folder. The workflow saves source coordinates, crop PNGs, contact sheets, indexes, a handwriting profile, and unresolved readings. Every claimed crop must come from an actual source image.

## Optional Ollama helper

`ollama_review.py` sends a target image and up to four user-verified reference crops to a running Ollama server. It saves the proposed reading separately and never changes the library's labels. Python 3.9+ and the standard library are sufficient for this helper.

```sh
python3 ollama_review.py --help
```

See [OLLAMA.md](OLLAMA.md) for examples, the required library fields, and the limits of direct model use. An image model agreeing with a label does not make that label verified. Recognition accuracy is not established by this repository.

## Files

- [SKILL.md](SKILL.md): the complete workflow and evidence rules.
- [OLLAMA.md](OLLAMA.md): local-model setup and examples.
- [ollama_review.py](ollama_review.py): optional review helper.

This repository contains the reusable method and helper. Bring your own manuscript images and corrections; no diary photographs or transcripts are included.
