"""Collect publicly displayed article metadata for human source review."""
from pathlib import Path
import re, html, json
from datetime import datetime
ROOT = Path(__file__).resolve().parents[1]
def clean(s):
    return html.unescape(re.sub('<[^>]+>', '', s)).strip()
out = {}
for p in (ROOT/'research/news-cache').glob('*.html'):
    body = p.read_text()
    items = []
    for m in re.finditer(r'<h3[^>]*>.*?</h3>', body, re.S):
        a = re.search(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',m.group(),re.S)
        if not a or not a.group(1).startswith('https://'): continue
        after = body[m.end():m.end()+2800]
        excerpt = re.search(r'<p[^>]*>(.*?)</p>',after,re.S)
        stamp = re.search(r'<div[^>]+title="([A-Z][a-z]+ \d+, \d{4})[^"\n]*"[^>]*>(.*?)</div>',after,re.S)
        if not stamp: continue
        day = datetime.strptime(stamp.group(1),'%b %d, %Y').date().isoformat()
        source = clean(stamp.group(2)).split(' - ')[-1]
        items.append({'date':day,'title':clean(a.group(2)),'summary':clean(excerpt.group(1)) if excerpt else '', 'url':html.unescape(a.group(1)),'source':source})
    out[p.stem.replace('MOG.A','MOG/A')] = items
(ROOT/'research/news-index.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print({k:len(v) for k,v in sorted(out.items())})
