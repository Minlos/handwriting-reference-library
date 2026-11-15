from pathlib import Path
import json,hashlib,datetime
R=Path(__file__).resolve().parent
notes={
17:['All five pages inspected for document correspondence; two essays continue through page5. No replacement-level mismatch found.'],
18:['Published text starts with an extra standalone title “Роль фамилии в жизни человека”; scan begins directly “Роль фамилии в жизни человека — вот проблема...”.','Published “общественно значимым” versus scan apparently “общественно значимый”; provisional AI audit, requires human review.','Published “радостямижизни” is joined, scan appears spaced.'],
20:['Two consecutive essays correspond across all five pages. Published text has joined document boundary “качеств.Родители”; primary gold unchanged.'],
21:['Page2 visibly repeats the phrase about “влиянии современного телевидения на зрителей” before “вот проблема”; published text has it once.','Published standalone heading “О влиянии современного телевидения на зрителей” has no corresponding separate heading at this boundary in page2.','Page3 title of the cited work differs visually from published “Головная боль”; uncertain exact written title, flag only.'],
22:['Page2 to page3 abruptly switches from a Родина essay to “Шоссе Россию здесь и тут...” as in published document; retain whole document.','Published separate question “Какие книги достойны внимания истинного читателя?” corresponds to scan; do not treat as spurious heading.'],
23:['Seven pages correspond to the two published essays and complete ending. Source and target share one eight-word sequence in prior mechanical audit; not a repeated target document.'],
24:['Page2 appears to omit numeric prefix “10.” from published heading “10. Судьба книги ...”; requires human review.','Four pages correspond to both published essays and complete ending.'],
25:['Four pages correspond to two published essays; target/source scan contrast is low.','Author surname in first essay visually uncertain versus published “Таня Гром”; no exact automatic correction adopted.'],
26:['Both pages correspond to full two-essay text; page2 continues paragraph begun on page1.','Published quote says “делами и делают оружие красивым”; scan appears “делали и делают оружие красивым”. Proposed literal difference provisional and not adopted into primary gold.'],
28:['All seven pages correspond to two published essays and complete ending; no replacement-level mismatch found.']}
records=[]
for w,flags in notes.items():
 gold=R/'evaluator'/'published'/f'writer{w:03}.txt';pages=json.loads((R/'groups'/f'writer{w:03}'/'targets.json').read_text())['pages']
 records.append(dict(writer=w,target_pages_inspected=[p['id'] for p in pages],inspection='All target pages visually surveyed in evaluator-only contact sheets; first source and target page compared for handwriting consistency. This is an assistant correspondence audit, not exhaustive human proofreading.',published_sha256=hashlib.sha256(gold.read_bytes()).hexdigest(),handwriting_attribution='visually consistent at survey level; dataset attribution retained; not forensic verification',eligibility='retain',flags=flags))
audit=dict(frozen_before_recognition=True,frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),label_status='published, not human-verified',primary='Published labels unchanged, including clear copying/text differences.',secondary_sensitivity_labels='Not created: uncertain full literal corrections are flags, not validated replacement gold.',records=records)
p=R/'evaluator'/'preinference-audit.json';assert not p.exists();p.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
(R/'evaluator'/'audit-freeze.json').write_text(json.dumps({'audit_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'gold_sha256':{str(x['writer']):x['published_sha256'] for x in records}},indent=2)+'\n')
print('Froze audit for',len(records),'writers; all 45 target pages surveyed; no replacements.')
