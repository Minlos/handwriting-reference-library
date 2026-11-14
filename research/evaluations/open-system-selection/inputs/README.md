# Nine public scans from nine writers

These images support a comparison of OCR systems and plain or reading-skill-assisted LLM recognition. They do not form a same-author reference collection. No extracted handwriting examples were supplied in this comparison.

The source is [HWR200](https://huggingface.co/datasets/AntiplagiatCompany/HWR200), pinned at revision `366a882a2b8d043d437126d2878bd3812ec55a94`. Selection includes every complete single-scan document in the downloaded subset, based on metadata rather than recognition results. Every tested system receives identical original file bytes; [the input manifest](../inputs.json) records their SHA256 hashes and source paths.

| Local scan | Upstream writer | Supplied source text |
|---|---|---|
| [writer009.jpg](writer009.jpg) | 009 | original9 |
| [writer015.png](writer015.png) | 015 | original15 |
| [writer035.jpg](writer035.jpg) | 035 | original0 |
| [writer037.png](writer037.png) | 037 | original2 |
| [writer040.jpg](writer040.jpg) | 040 | original5 |
| [writer065.jpg](writer065.jpg) | 065 | original30 |
| [writer072.jpeg](writer072.jpeg) | 072 | original2 |
| [writer080.jpg](writer080.jpg) | 080 | original10 |
| [writer153.jpg](writer153.jpg) | 153 | original13 |

There are eight distinct source texts: writers 037 and 072 copied the same text. Supplied full-document texts are scoring references, not independently verified transcriptions of every visible mark. Copying differences can therefore count as recognition errors. The selection is small and does not establish performance on a population of writers or the benefit of same-author references.

See [the comparison and its limitations](../README.md) for measured results, model settings and access failures.
