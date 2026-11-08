# Original assistant reading of page 6: measured against user corrections

The saved first draft is evaluated against the user-reviewed wording, including the latest correction «заработаешь». The final uncertain «кракушку?» is excluded from both texts; the known prefix remains scored.

| Metric | Edits / reference units | Error rate |
|---|---:|---:|
| CER, case and punctuation retained | 12 / 520 characters | 2.31% |
| CER, case and punctuation ignored | 12 / 471 characters | 2.55% |
| WER, case and punctuation ignored | 3 / 85 words | 3.53% |

Word errors:
- substitution: 'зарабатываешь' → 'заработаешь'
- substitution: 'деньги' → 'десять'
- deletion: '' → 'тысяч'

Unicode NFC and whitespace normalization are used throughout; ё is not merged with е. The date is included. Uncertainty markers are annotations: «[Танюшка?]» counts as an attempted correct word. The first unread word, now confirmed as «тысяч», counts as missing text.

Reference partly derives from user acceptance of the draft, not independent transcription. This is not a blind GPT-model comparison or a corpus-wide accuracy estimate.
