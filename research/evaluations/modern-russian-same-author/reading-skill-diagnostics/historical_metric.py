"""Score complete frozen documents, with paired bootstrap resampling of writers."""
import argparse
import csv
import hashlib
import json
import random
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONDITIONS = ('A', 'B', 'C', 'D')


def normalize(text, mode='literal'):
    text = unicodedata.normalize('NFC', text)
    if mode == 'reading':
        text = ''.join(c for c in text.casefold()
                       if not unicodedata.category(c).startswith('P'))
    return ' '.join(text.split())


def distance(a, b):
    """Myers bit-vector Levenshtein; handles Unicode code points or word tokens."""
    if not a:
        return len(b)
    matches = {}
    for i, token in enumerate(a):
        matches[token] = matches.get(token, 0) | (1 << i)
    full = (1 << len(a)) - 1
    high = 1 << (len(a) - 1)
    positive, negative, result = full, 0, len(a)
    for token in b:
        equal = matches.get(token, 0)
        vertical = equal | negative
        horizontal = (((equal & positive) + positive) ^ positive) | equal
        ph = negative | ~(horizontal | positive)
        mh = positive & horizontal
        result += bool(ph & high) - bool(mh & high)
        ph = (ph << 1) | 1
        mh <<= 1
        positive = (mh | ~(vertical | ph)) & full
        negative = ph & vertical & full
    return result


def score(ref, hyp, mode):
    a, b = normalize(ref, mode), normalize(hyp, mode)
    aw, bw = a.split(), b.split()
    edits, word_edits = distance(a, b), distance(aw, bw)
    return dict(edits=edits, characters=len(a), cer=edits / len(a),
                word_edits=word_edits, words=len(aw), wer=word_edits / len(aw))


def aggregate(rows, condition, mode):
    selected = [r[mode] for r in rows if r['condition'] == condition]
    totals = {k: sum(r[k] for r in selected)
              for k in ('edits', 'characters', 'word_edits', 'words')}
    totals.update(cer=totals['edits'] / totals['characters'],
                  wer=totals['word_edits'] / totals['words'])
    return totals


def bootstrap(rows, writers, repetitions=10000):
    lookup = {(r['condition'], r['writer']): r['literal'] for r in rows}
    rng = random.Random(20261112)
    values = {c: [] for c in ('B', 'C', 'D')}
    extra_pairs = {'D_vs_C': [], 'D_vs_B': []}
    for _ in range(repetitions):
        sample = rng.choices(writers, k=len(writers))
        base = sum(lookup['A', w]['edits'] for w in sample)
        for condition in values:
            edits = sum(lookup[condition, w]['edits'] for w in sample)
            values[condition].append(100 * (1 - edits / base) if base else 0)
        for key in extra_pairs:
            condition, baseline = key.split('_vs_')
            numerator = sum(lookup[condition, w]['edits'] for w in sample)
            denominator = sum(lookup[baseline, w]['edits'] for w in sample)
            extra_pairs[key].append(100 * (1 - numerator / denominator) if denominator else 0)
    result = {}
    for condition, samples in values.items():
        samples.sort()
        wins = sum(lookup[condition, w]['cer'] < lookup['A', w]['cer'] for w in writers)
        ties = sum(lookup[condition, w]['cer'] == lookup['A', w]['cer'] for w in writers)
        result[condition] = dict(
            relative_error_reduction_percentile_2_5=samples[int(repetitions * .025)],
            relative_error_reduction_percentile_97_5=samples[int(repetitions * .975)],
            writers_better_than_A=wins, writers_equal_to_A=ties,
            writers_worse_than_A=len(writers)-wins-ties)
    additional = {}
    for key, samples in extra_pairs.items():
        condition, baseline = key.split('_vs_')
        samples.sort()
        additional[key] = dict(
            relative_error_reduction_percentile_2_5=samples[int(repetitions * .025)],
            relative_error_reduction_percentile_97_5=samples[int(repetitions * .975)],
            writers_better=sum(lookup[condition,w]['edits'] < lookup[baseline,w]['edits'] for w in writers),
            writers_equal=sum(lookup[condition,w]['edits'] == lookup[baseline,w]['edits'] for w in writers))
    return dict(unit='writer', paired=True, repetitions=repetitions,
                seed=20261112, estimates=result,
                additional_pairs=additional,
                limitation='Writers selected deterministically, one run per condition; resampling measures writer sensitivity, not model run variance or population representativeness.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--partial', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    rows, missing = [], []
    for condition in CONDITIONS:
        for batch in (1, 2):
            status = ROOT / f'predictions/{condition}/status-batch{batch}.json'
            if not status.exists():
                missing.append(str(status.relative_to(ROOT)))
        for writer in manifest['writers']:
            path = ROOT / f'predictions/{condition}/writer{writer:03}.txt'
            if not path.exists():
                missing.append(str(path.relative_to(ROOT)))
                continue
            expected = [s for s in manifest['samples']
                        if s['role'] == 'target' and s['writer'] == writer]
            page_files = [ROOT / f'predictions/{condition}/writer{writer:03}' /
                          (Path(s['local']).stem + '.txt') for s in expected]
            absent = [str(f.relative_to(ROOT)) for f in page_files if not f.exists()]
            if absent:
                missing.extend(absent)
                continue
            ref = (ROOT / f'evaluator/writer{writer:03}.txt').read_text()
            hyp = path.read_text()
            if not hyp.strip():
                raise ValueError(f'Empty prediction {path}')
            rows.append(dict(condition=condition, writer=writer,
                             target_pages=len(expected),
                             unknown_markers=hyp.casefold().count('[неразборчиво]'),
                             prediction_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                             **{mode: score(ref, hyp, mode) for mode in ('literal', 'reading')}))
    if missing and not args.partial:
        raise RuntimeError(f'{len(missing)} predictions missing; refusing an incomplete combined report')
    aggregates = [dict(condition=c, writers=sum(r['condition'] == c for r in rows),
                       unknown_markers=sum(r['unknown_markers'] for r in rows if r['condition'] == c),
                       **{mode: aggregate(rows, c, mode) for mode in ('literal', 'reading')})
                  for c in CONDITIONS if any(r['condition'] == c for r in rows)]
    result = dict(status='partial' if missing else 'complete', missing=missing,
                  source='Official full_text labels for each complete original document; no visual corrections applied.',
                  model='gpt-6.1-sol', target_pages=manifest['target_pages'],
                  normalization={'literal': 'NFC; whitespace collapse; case and punctuation retained',
                                 'reading': 'NFC; casefold; Unicode punctuation removed; whitespace collapse; ё retained'},
                  writers=rows, aggregates=aggregates)
    if not missing:
        result['writer_bootstrap'] = bootstrap(rows, manifest['writers'])
        sensitivity = []
        for omitted in manifest['writers']:
            selected = [r for r in rows if r['writer'] != omitted]
            values = {c: aggregate(selected, c, 'literal') for c in CONDITIONS}
            sensitivity.append(dict(omitted_writer=omitted, aggregates=values,
                relative_error_reduction_vs_A={c:100*(1-values[c]['edits']/values['A']['edits']) for c in 'BCD'}))
        result['leave_one_writer_out'] = sensitivity
    name = 'partial-metrics' if missing else 'metrics'
    (ROOT / f'{name}.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    with (ROOT / f'{name}.csv').open('w') as f:
        out = csv.writer(f)
        out.writerow(['condition', 'writers', 'edits', 'characters', 'literal_CER_percent',
                      'reading_CER_percent', 'reading_WER_percent'])
        for r in aggregates:
            out.writerow([r['condition'], r['writers'], r['literal']['edits'],
                          r['literal']['characters'], 100*r['literal']['cer'],
                          100*r['reading']['cer'], 100*r['reading']['wer']])
    print((ROOT / f'{name}.csv').read_text())


if __name__ == '__main__':
    main()
