# Portable handwriting skill revision

The current skill separates image-reading decisions from host operations and treats reference assistance as optional evidence. It is general-purpose Markdown for suitable LLM hosts, not a GPT-specific workflow. A text-only model can coordinate an OCR/vision workflow but cannot claim visual inspection itself.

The revision follows the supplied handwriting-skill-critique.md. It adopts the supported design corrections without treating its hypotheses as measured causes:

- Product-mode instructions and operational file procedures moved out of the model-facing core into HOST.md. Image-capable single calls no longer need to pretend to execute file tools or switch application modes.
- Mandatory library/profile loading became selective reference use. The model may ignore irrelevant, conflicting or confusing examples. It records only comparisons actually made.
- Tool-using agents and prompt-only inference are explicitly distinguished. Reference selection and presentation remain host responsibilities.
- The local runner now supplies the handwriting profile only with `--include-profile`. It remains a hypothesis tied to examples, not target ground truth.
- Human confirmation, provisional readings, unresolved spans, source pixels, category boundaries and preservation of odd child wording remain essential rules.

The critique's suggested concrete child-word example was not embedded in the new model instructions: that word occurs in an existing test page and would leak a target answer into a purportedly blind condition. The rule remains general. Likewise, no fixed number of reference crops is declared optimal; the proposed selection/presentation experiments have not established one.

The earlier Sol gain changed both instructions and reference access. Gemma's fixed-reference condition regressed, but the mechanism is unknown. The supplied critique describes Grok as pending; the completed earlier Grok run measured 137 versus 132 errors (9.45% versus 9.11% reading CER) with the same three example pages in both conditions. That small one-trial gain does not prove a universal skill benefit.

All previous benchmark skill snapshots and scores remain unchanged. The separate four-condition handoff freezes the revised skill and uses different reference/target pages. New setup changes, such as plaintext output and local context length, must not be mistaken for an isolated old-versus-new skill comparison. Validation of file operations and prompt construction is not recognition-accuracy validation.

See SKILL.md for model guidance, HOST.md for host duties, LOCAL.md for optional local execution, and handoffs/skill-reference-evaluation/ for the reproducible comparison protocol. No fine-tuning is performed.

The current collection workflow requires a provisional reading of every supplied image, collection-wide evidence comparison, available OCR candidates, and full rereading cycles. It records pass coverage and supported changes, checks crop boundaries, and stops after a full pass yields no supported changes or an explicit limit is reached. The standalone extraction skill follows the same cycle. This revision has structural validation; its effect on recognition accuracy has not been measured.
