import os
import re

html_files = [
    'index.html',
    'germany/index.html',
    'germany/german-weather.html',
    'germany/german-sick.html'
]

# Map absolute path prefixes to relative links based on directory depth
for filepath in html_files:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '/' in filepath:
        # In a subfolder
        root_prefix = '../'
    else:
        # In root folder
        root_prefix = './'

    def replacer(match):
        path = match.group(1)
        if path == '/':
            return f'"{root_prefix}index.html"'
        if path.startswith('/germany/'):
            rem = path[len('/germany/'):]
            if not rem: rem = 'index.html'
            if root_prefix == '../': return f'"./{rem}"'
            else: return f'"./germany/{rem}"'
        if path.startswith('/ai/'):
            return f'"{root_prefix}ai/index.html"'
        if path.startswith('/playlog/'):
            return f'"{root_prefix}playlog/index.html"'
        if path.startswith('/games/'):
            return f'"{root_prefix}games/index.html"'
        if path.startswith('/psychology/'):
            return f'"{root_prefix}psychology/index.html"'
        if path.startswith('/about/'):
            return f'"{root_prefix}about/index.html"'
        return match.group(0)

    # regex to match href="/..."
    new_content = re.sub(r'"(/[^"]*)"', replacer, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
