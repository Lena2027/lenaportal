"""
Scans germany/*.html and generates posts.json
Run from repo root: python3 scripts/scan_posts.py
"""
import re, glob, json, os
from datetime import datetime

files = [f for f in sorted(glob.glob('germany/*.html')) if 'index' not in f]
posts = []

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()

    # Title: from <title> tag, strip site suffix
    title_m = re.search(r'<title>([^<]+)</title>', c)
    title = title_m.group(1).strip() if title_m else ''
    # Remove common suffixes
    for suffix in [' | lena-var4', ' | lena-var4.com', ' – lena-var4.com',
                   ' | 독일 일상 블로그', ' | 독일 일상', ' | Lena의 독일 일상', ' | Lena의 독일 생활']:
        title = title.replace(suffix, '')
    title = title.strip()

    # Date: prefer datePublished JSON-LD, fallback to article:published_time meta
    date_str = ''
    date_m = re.search(r'"datePublished":\s*"([^"]{10})', c)
    if date_m:
        date_str = date_m.group(1)[:10]
    else:
        date_m2 = re.search(r'article:published_time.*?content="([^"]{10})', c)
        if date_m2:
            date_str = date_m2.group(1)[:10]

    # Category
    category = '🇩🇪 Germany'

    # dateDisplay (e.g. "Apr 2026")
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        date_display = dt.strftime('%b %Y')
    except:
        date_display = ''

    # Tag: first sidebar-tag or first keyword
    tags = re.findall(r'class="sidebar-tag[^"]*">([^<]+)</a>', c)
    kw_m = re.search(r'"keywords":\s*"([^"]+)"', c)
    if tags:
        tag = '#' + tags[0].strip().replace(' ', '').replace('#', '')
    elif kw_m:
        first_kw = kw_m.group(1).split(',')[0].strip()
        tag = '#' + first_kw.replace(' ', '')
    else:
        tag = '#독일'

    url = './' + f.replace('\\', '/')

    posts.append({
        'url': url,
        'title': title,
        'category': category,
        'date': date_str,
        'dateDisplay': date_display,
        'tag': tag
    })

# Sort by date descending (no date goes to end)
posts.sort(key=lambda p: p['date'] if p['date'] else '0000', reverse=True)

with open('posts.json', 'w', encoding='utf-8') as out:
    json.dump(posts, out, ensure_ascii=False, indent=2)

print(f'Generated posts.json with {len(posts)} posts')
for p in posts[:5]:
    print(f"  {p['date']} | {p['title'][:40]} | {p['tag']}")
