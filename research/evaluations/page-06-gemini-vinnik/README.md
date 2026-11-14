# Gemini + Vinnik: supplied page 6 transcription

The user identified this supplied text as Gemini + Vinnik. Its exact model version, prompt and reference context are unknown. The same user-corrected page-6 reference and uncertain-final-span exclusion are used as in the assistant comparison. Invisible copy/paste format characters are removed.

| Metric | Edits / reference units | Rate |
|---|---:|---:|
| CER retaining case and punctuation | 52 / 520 characters | 10.00% |
| CER ignoring case and punctuation | 19 / 471 characters | 4.03% |
| WER ignoring case and punctuation | 8 / 85 words | 9.41% |

Word errors:
- 'денег' → 'десять' (substitution)
- 'я' → 'а' (substitution)
- 'ешь' → 'ест' (substitution)
- 'папа' → 'таня' (substitution)
- 'папа' → 'таня' (substitution)
- 'папа' → 'мама' (substitution)
- 'танечка' → 'танюшка' (substitution)
- 'ромбик' → 'ротик' (substitution)

Same corrected page-6 reference as the original assistant draft, but different workflows and unknown Gemini conditions. This is not a controlled causal estimate of skill benefit.

## Conventional OCR on the matching test material

| Evaluated material | Tesseract 5.5.4, Russian best | EasyOCR 1.7.2, Cyrillic |
|---|---:|---:|
| Page 6, final unknown word excluded | 75.80% (357/471) | 87.69% (413/471) |

The conventional baseline uses the frozen page-6 target region. The original contextual/external workflow cannot establish identical call inputs and effort.
These are new local OCR measurements, not substituted LLM results. Raw outputs, setup, scope adapters and per-target counts are in the [conventional OCR report](../conventional-baselines/README.md).
