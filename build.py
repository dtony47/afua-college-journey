#!/usr/bin/env python3
"""Build index.html from template.html + data.json (data embedded, so index.html is fully self-contained).

Usage:  python3 build.py            # validates data.json, writes index.html
"""
import json, re, sys, pathlib
here = pathlib.Path(__file__).parent
data = json.loads((here / 'data.json').read_text(encoding='utf-8'))

# --- light validation
errors = []
for k in ('colleges', 'events', 'tasks', 'activity'):
    if not isinstance(data.get(k), list): errors.append(f'missing list: {k}')
date_re = re.compile(r'^\d{4}-\d{2}-\d{2}$')
for e in data.get('events', []):
    if not date_re.match(e.get('date', '')): errors.append(f"event {e.get('id')}: bad date {e.get('date')!r}")
for a in data.get('activity', []):
    if not date_re.match(a.get('date', '')) or not a.get('text'): errors.append(f'activity entry needs date YYYY-MM-DD and text: {a}')
for t in data.get('tasks', []):
    if t.get('due') and not date_re.match(t['due']): errors.append(f"task {t.get('id')}: bad due {t['due']!r}")

# --- privacy guard: refuse to publish obvious personal details
raw = json.dumps(data, ensure_ascii=False)
patterns = {
    'email address': r'[\w.+-]+@[\w-]+\.[\w.]+',
    'UK mobile number': r'(?:\+44\s?7|\b07)\d{3}\s?\d{6}\b',
    'UK postcode': r'\b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b',
}
for name, p in patterns.items():
    m = re.search(p, raw)
    if m: errors.append(f'privacy: looks like a {name} in data.json ({m.group(0)!r}); remove it before publishing')

if errors:
    print('Build failed:\n  - ' + '\n  - '.join(errors)); sys.exit(1)

tpl = (here / 'template.html').read_text(encoding='utf-8')
blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
out = re.sub(r'/\*DATA\*/.*?/\*END\*/', lambda _: '/*DATA*/' + blob + '/*END*/', tpl, count=1, flags=re.S)
(here / 'index.html').write_text(out, encoding='utf-8')
print(f"Built index.html: {len(data['colleges'])} colleges, {len(data['events'])} dates, "
      f"{len(data['tasks'])} tasks, {len(data['activity'])} log entries")
