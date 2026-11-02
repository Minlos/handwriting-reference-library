# Grok: effect of the skill with the same three example pages

Adding the skill produces **3.6% fewer character errors** in this single three-page run: 137 errors with examples alone, versus 132 with the same examples plus the skill. The gain is small and is not consistent across pages. No repeat-trial uncertainty estimate is available.

| Condition | Page 4 CER | Page 6 CER | Page 7 CER | All three pages CER |
|---|---:|---:|---:|---:|
| Grok + three example pages | 11.94% (61/511) | 9.34% (44/471) | 6.85% (32/467) | **9.45% (137/1449)** |
| Grok + same examples + skill | 11.74% (60/511) | 7.86% (37/471) | 7.49% (35/467) | **9.11% (132/1449)** |

The API reported a total charge of **$0.402454** for all six inference calls, within the user-authorized $3 limit. No inference requests were retried. Model availability checks did not generate completions.

Both conditions receive three full upright example-page images, pages 1–3, with the same 24 region-scoped user-confirmed excerpts. Other words on those pages are not labeled as verified. Each request then receives exactly one separate target image, page 4, 6 or 7. The test target byte hashes match the earlier Sol/Gemma experiments. Example-page working JPEGs are 1800×2400; transforms, coordinates, hashes and original source names are recorded.

The only condition change is the added complete SKILL.md text in the system message. The baseline already asks for faithful Russian transcription, preservation of odd child wording and uncertainty marking. Thus this measures the incremental benefit of the full skill **given the same examples and generic task instructions**, not the benefit of examples themselves. It is not directly comparable to Sol's 41.8% reduction, where both instructions and reference access changed.

Settings: `grok-4.7`, Responses API, low reasoning effort, temperature 0.7, top_p 0.95, visible-output limit 4096, high-detail image inputs, `store: false`, no search/tools and no conversation chaining. There is one stateless call per page per condition. Order alternates by target page. All six responses completed. Raw replies, token usage, reported exact per-call cost, elapsed time, prompt text and image hashes are retained. Prompt caching can affect cost and latency; no efficiency effect is inferred from the cost difference between conditions.

CER uses Unicode NFC and collapsed whitespace. The main reading score ignores case and Unicode punctuation; ё remains distinct from е. Only the final unresolved word on page 6 is excluded from both conditions; all known preceding text is scored, including wrongly read or illegible words. Exact excluded suffixes are saved separately. Aggregate CER sums edits and reference characters. Literal CER and word errors are retained in metrics.json.

Concrete examples:

- Page 6: examples alone reads «Танточика» where the confirmed word is «Танюшка». The skill condition reads «Танюшка» correctly.
- Page 7: both conditions normalize the confirmed child form «хочила» to «хотела» and read «французами» instead of «фашистами». Explicit preservation instructions did not prevent these errors.
- Page 7 gets worse overall with the skill: 32 becomes 35 character errors. For «Аллочка», examples alone reads «Анечка», while the skill condition reads «Аленочка»; neither is correct.

Pages 4 and 7 have human-confirmed wording; page 6 has one unresolved final word. Punctuation is editorial. All pages were already inspected in this project, and some reference text was confirmed by correcting earlier assistant drafts. This is calibration on known material, not an untouched independent validation. Temperature is nonzero and there is only one trial, so a five-character gain does not establish stable improvement on future pages.

The skill snapshot SHA-256 is `70045b10b9ece68a1d4aaf15cfacafdff5a525fc39dc0b59f74950f893035021`. Input-construction tests confirm that images, reference labels and generation settings match between the conditions, and that target corrections are absent from both prompts. The reading runner never opens scoring reference files.

Evidence: [metrics](metrics.json), [requests and replies](run.json), [three-page examples and confirmed-excerpt metadata](fixture.json), [source transforms](image-provenance.json), [page-6 mask](page-6-exclusions.json), [skill snapshot](SKILL.md). API access and usage billing are distinct from the Grok CLI subscription route; these are direct API results.
