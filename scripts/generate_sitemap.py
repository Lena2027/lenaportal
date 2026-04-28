"""
Generates sitemap.xml for lena-var4.com
Run from repo root: python3 scripts/generate_sitemap.py
"""
import re, glob, os
from datetime import datetime, timezone

BASE = "https://lena-var4.com"

# Priority + changefreq rules
RULES = {
    'index.html':               (1.0, 'weekly'),
    'about/index.html':         (0.8, 'monthly'),
    'privacy-policy.html':      (0.3, 'yearly'),
    'germany/index.html':       (0.9, 'daily'),
    'en/index.html':            (0.8, 'weekly'),
    'en/germany/index.html':    (0.7, 'weekly'),
}
GERMANY_POST  = (0.8, 'monthly')
DEFAULT_RULE  = (0.5, 'monthly')

def get_lastmod(filepath):
    """Extract datePublished from HTML, else use file mtime."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            c = f.read()
        m = re.search(r'"datePublished":\s*"([^"]{10})', c)
        if m:
            return m.group(1)[:10]
    except:
        pass
    mtime = os.path.getmtime(filepath)
    return datetime.fromtimestamp(mtime, tz=timezone.utc).strftime('%Y-%m-%d')

def path_to_url(filepath):
    p = filepath.replace('\\', '/')
    if p == 'index.html':
        return BASE + '/'
    if p.endswith('/index.html'):
        return BASE + '/' + p[:-len('index.html')]
    return BASE + '/' + p

# Collect pages
pages = []

# Priority pages first
priority_files = [
    'index.html',
    'about/index.html',
    'germany/index.html',
    'en/index.html',
    'en/germany/index.html',
    'privacy-policy.html',
]
for f in priority_files:
    if os.path.exists(f):
        pages.append(f)

# Germany posts
for f in sorted(glob.glob('germany/*.html')):
    if f not in pages and 'index' not in f:
        pages.append(f)

# EN posts
for f in sorted(glob.glob('en/germany/*.html')):
    if f not in pages and 'index' not in f:
        pages.append(f)

# Build XML
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']

for filepath in pages:
    norm = filepath.replace('\\', '/')
    url = path_to_url(norm)
    lastmod = get_lastmod(filepath)

    # Determine priority/changefreq
    if norm in RULES:
        priority, changefreq = RULES[norm]
    elif norm.startswith('germany/') and norm != 'germany/index.html':
        priority, changefreq = GERMANY_POST
    else:
        priority, changefreq = DEFAULT_RULE

    lines.append('  <url>')
    lines.append(f'    <loc>{url}</loc>')
    lines.append(f'    <lastmod>{lastmod}</lastmod>')
    lines.append(f'    <changefreq>{changefreq}</changefreq>')
    lines.append(f'    <priority>{priority}</priority>')
    lines.append('  </url>')

lines.append('</urlset>')

sitemap = '\n'.join(lines) + '\n'
with open('sitemap.xml', 'w', encoding='utf-8') as out:
    out.write(sitemap)

print(f"Generated sitemap.xml with {len(pages)} URLs")
for p in pages[:6]:
    print(f"  {path_to_url(p.replace(chr(92),'/'))} [{get_lastmod(p)}]")
if len(pages) > 6:
    print(f"  ... and {len(pages)-6} more")
