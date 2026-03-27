import os
import shutil
import re

html_files = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or '.gemini' in root or 'en' in root.split(os.sep) or 'assets' in root.split(os.sep):
        continue
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.normpath(os.path.join(root, f))
            # skip already 'en' folder incorrectly parsed
            if 'en\\' in filepath or 'en/' in filepath.replace('\\', '/'): continue
            html_files.append(filepath)

# Create EN copies
for f in html_files:
    en_path = os.path.join('en', f.replace('.\\', '').replace('./', ''))
    os.makedirs(os.path.dirname(en_path), exist_ok=True)
    shutil.copy2(f, en_path)

# Collect all files to update
all_files = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or '.gemini' in root or 'assets' in root.split(os.sep):
        continue
    for f in files:
        if f.endswith('.html'):
            all_files.append(os.path.normpath(os.path.join(root, f)))

for f in all_files:
    parts = f.replace('.\\', '').replace('./', '').split(os.sep)
    is_en = parts[0] == 'en'
    
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Skip if already has language switch
    if '>🇬🇧 EN</a>' in content or '>🇰🇷 KO</a>' in content:
        continue

    if is_en:
        # Depth calculation from 'en'
        sub_path = parts[1:]
        sub_depth = len(sub_path) - 1
        prefix = '../' * (sub_depth + 1)
        if not prefix: prefix = './'
        target_href = prefix + '/'.join(sub_path)
        lang_html = f'<li><a href="{target_href}">🇰🇷 KO</a></li>'
    else:
        # Original (KO) file
        sub_path = parts
        sub_depth = len(sub_path) - 1
        prefix = '../' * sub_depth if sub_depth > 0 else './'
        target_href = prefix + 'en/' + '/'.join(sub_path)
        lang_html = f'<li><a href="{target_href}">🇬🇧 EN</a></li>'
    
    # Inject into the navbar
    match = re.search(r'(<ul class="nav-links">.*?)(</ul>)', content, flags=re.DOTALL)
    if match:
        ul_content = match.group(1)
        ul_end = match.group(2)
        new_content = content[:match.start()] + ul_content + '  ' + lang_html + '\n    ' + ul_end + content[match.end():]
        content = new_content
        
    # Translate EN index.html elements
    if is_en and 'index.html' in parts and len(parts) == 2:
        content = content.replace('독일 생활 솔직 후기. 날씨부터 비자까지, 아무도 알려주지 않는 것들을 씁니다.', 'Honest reviews of life in Germany. From weather to visas, things no one tells you.')
        content = content.replace('AI 툴로 혼자 만들고, 자동화하고, 돈 버는 이야기. 솔직하게 씁니다.', 'Solo building, automating, and making money with AI tools. Written honestly.')
        content = content.replace('내가 직접 해본 게임들의 리뷰, 공략, 추천. 취향 필터 없이 솔직하게 씁니다.', 'Game reviews, guides, and recommendations. Honest opinions without filters.')
        content = content.replace('직접 만든 웹 게임들. 숨은그림찾기부터 시작해서 어디까지 갈지 모르겠어요.', 'Web games made by myself. Starting with hidden object games, not sure where it will go.')
        content = content.replace('심리 테스트와 마음 이야기. SOULCAKEY에서 시작된 것들이 여기 모입니다.', 'Psychology tests and mind talks. Everything started from SOULCAKEY gathers here.')
        content = content.replace('독일에 사는 한국인 솔로 빌더. AI, 게임, 글쓰기로 인터넷에서 뭔가를 만들고 있습니다.', 'Korean solo builder living in Germany. Making things on the internet with AI, games, and writing.')
        content = content.replace('Lidl 호두꿀빵, 올해도 나를 비껴갔다', 'Lidl Honey Walnut Bread, missed me again this year')
        content = content.replace('독일에서 아프면 각오해야 한다', 'Be prepared if you get sick in Germany')
        content = content.replace('독일 날씨가 미쳤다 — 정신병자인 이유 8가지', 'German weather is crazy — 8 reasons why it is psychotic')
        # Also fix hreflang? It's fine for now, user just asked for separation
        content = content.replace('lang="ko"', 'lang="en"')

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print(f"Processed {len(all_files)} files into en/ and updated links.")
