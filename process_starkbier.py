import os
import re

base_path = 'germany/german-weather.html'
raw_path = 'germany/munich-starkbierfest.html'

with open(base_path, 'r', encoding='utf-8') as f:
    template = f.read()

with open(raw_path, 'r', encoding='utf-8') as f:
    raw = f.read()

# 1. Extract raw parts
title_match = re.search(r'<title>(.*?)</title>', raw)
new_title = title_match.group(1) if title_match else '뮌헨 강한 맥주 축제 슈타르크비어페스트 완벽 가이드 2026 | Germany Blog — lena-var4'

desc_match = re.search(r'<meta name="description" content="(.*?)">', raw)
new_desc = desc_match.group(1) if desc_match else '3월 뮌헨에서만 맛볼 수 있는 강한 맥주 축제의 모든 것.'

style_match = re.search(r'<style>(.*?)</style>', raw, re.DOTALL)
new_style = style_match.group(1) if style_match else ''
new_style = re.sub(r'body\s*{[^}]*}', '', new_style)
new_style = re.sub(r'\*\s*{[^}]*}', '', new_style)
new_style = new_style.replace('.hero', '.stark-hero').replace('article {', '.stark-article {')

hero_match = re.search(r'<header class="hero">(.*?)</header>', raw, re.DOTALL)
new_hero = '<div class="stark-hero hero">' + hero_match.group(1) + '</div>' if hero_match else ''

article_match = re.search(r'<article>(.*?)</article>', raw, re.DOTALL)
new_article = '<article class="article stark-article">' + article_match.group(1) + '</article>' if article_match else ''

# 2. Inject into template
template = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', template)
template = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{new_desc}">', template)
template = template.replace('</style>', new_style + '\n  </style>')
template = re.sub(r'<!-- ═══ WEATHER HERO ═══ -->.*?<!-- ═══ 글 \+ 사이드바 ═══ -->', 
                  '<!-- ═══ STARKBIER HERO ═══ -->\n    ' + new_hero + '\n\n    <!-- ═══ 글 + 사이드바 ═══ -->', 
                  template, flags=re.DOTALL)
template = re.sub(r'<article class="article">.*?</article>', new_article, template, flags=re.DOTALL)

template = re.sub(r'<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{new_title}">', template)
template = re.sub(r'<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{new_desc}">', template)
template = re.sub(r'<meta name="twitter:title" content=".*?">', f'<meta name="twitter:title" content="{new_title}">', template)
template = re.sub(r'<meta name="twitter:description" content=".*?">', f'<meta name="twitter:description" content="{new_desc}">', template)
template = re.sub(r'<meta property="og:url" content=".*?">', '<meta property="og:url" content="https://lena2027.github.io/lenaportal/germany/munich-starkbierfest.html">', template)

# The sidebar in the template needs to have its "current" class updated.
template = template.replace('class="current"', '')
# We will inject the new post into the sidebar later for all files at once.

with open(raw_path, 'w', encoding='utf-8') as f:
    f.write(template)

print("munich-starkbierfest.html formatted successfully!")
