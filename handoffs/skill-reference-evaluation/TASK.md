# Task for another evaluator or LLM host

Evaluate the handwriting skill and author references independently using the four-condition protocol in this folder. You are the coordinator, not the model being tested. Read README.md and protocol.json, validate the source images, then export blind packets with prepare_inputs.py. Use a fresh context for every primary reading. Give the tested model only its packet; do not inherit this conversation, gold/, repository access, global copies of the skill or prior corrected target text.

Run A (neither factor), B (skill only), C (references only), D (both) on the same six targets, with the same model/runtime settings and output format. The references are pages 4,6,7; targets are 1,2,3,5,8,9. Use actual image attachments and only the specified texts. Do not add a profile, OCR candidate or new reference in just one condition. Do not assume the current skill or reference condition will win.

Use an explicitly authorized model/setup and budget. Do not request or publish credentials in a prompt. Preserve all first attempts and mark unsupported interfaces honestly. If you have already seen the gold text, do not perform a supposedly blind reading in your own existing context; dispatch independent requests with only the allowed packet.

Fill results-template.jsonl, keep raw replies and exact request metadata, and score using score_results.py. The reading runner must not open gold files. Return a single table with per-page and total errors/denominators, coverage, A→B and C→D skill effects, A→C and B→D reference effects, and actual cost. Show at least one regression or persistent error when present. State the small calibration sample and any host limitations. Do not claim training, independent held-out validation or guaranteed accuracy.
