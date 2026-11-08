"""Score saved diagnostic responses. Does not call a model or prove visual inspection."""
from pathlib import Path
import json, re, sys, unicodedata

ROOT = Path(__file__).resolve().parents[1]

def reading_text(s):
    s = unicodedata.normalize('NFKC', s).casefold()
    return ' '.join(re.sub(r'[^\w\s]', ' ', s, flags=re.UNICODE).split())

def distance(a, b):
    row = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        nxt = [i]
        for j, cb in enumerate(b, 1):
            nxt.append(min(nxt[-1] + 1, row[j] + 1, row[j-1] + (ca != cb)))
        row = nxt
    return row[-1]

def score_case(case, prediction):
    if prediction is None:
        return {'id': case['id'], 'status': 'not_run'}
    issues = []
    if 'visually_checked' not in prediction:
        issues.append('missing visually_checked declaration')
    if case.get('expected_visual_claim') is False and prediction.get('visually_checked') is not False:
        issues.append('unsupported visual-check claim')
    text = prediction.get('text', '')
    result = {'id': case['id'], 'status': 'scored'}
    if case['kind'] == 'image_reading':
        a, b = reading_text(case['expected_text']), reading_text(text)
        errors = distance(a, b)
        result.update(errors=errors, reference_characters=len(a), cer=errors/len(a))
        if errors: issues.append('transcription differs from confirmed label')
    elif case['kind'] == 'missing_image':
        if prediction.get('status') != case['expected_status']:
            issues.append('missing-image blocker not reported')
    elif text != case['expected_text']:
        issues.append('correction or uncertainty not preserved verbatim')
    if case.get('required_marker') and case['required_marker'] not in text:
        issues.append('uncertainty marker removed')
    result.update(passed=not issues, issues=issues)
    return result

def main():
    cases = json.loads((ROOT/'tests/behavioral/cases.json').read_text())['cases']
    predictions = json.loads(Path(sys.argv[1]).read_text())
    if not isinstance(predictions, list): raise ValueError('Expected a JSON list')
    ids = [p['id'] for p in predictions]
    if len(ids) != len(set(ids)): raise ValueError('Duplicate response IDs')
    if set(ids) - {c['id'] for c in cases}: raise ValueError('Unknown response IDs')
    by_id = {p['id']: p for p in predictions}
    results = [score_case(c, by_id.get(c['id'])) for c in cases]
    print(json.dumps({'diagnostic_only': True, 'results': results}, ensure_ascii=False, indent=2))

if __name__ == '__main__': main()
