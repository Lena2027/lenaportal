import re
import os

paths = ['germany/munich-starkbierfest.html', 'en/germany/munich-starkbierfest.html']
for p in paths:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<meta property="article:published_time" content=".*?">', '<meta property="article:published_time" content="2026-03-27T00:00:00Z">', c)
    c = re.sub(r'"datePublished":\s*".*?"', '"datePublished": "2026-03-27T00:00:00Z"', c)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

os.system('python publish.py')
print("Dates fixed and publish.py re-run successfully.")
