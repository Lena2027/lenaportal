import os
import shutil

html_files = [
    'index.html',
    'en/index.html',
    'germany/index.html',
    'germany/german-weather.html',
    'germany/german-sick.html',
    'germany/lidl-walnuss-honig-brot-v2.html',
    'germany/munich-starkbierfest.html'
]

# 1. First, make sure en/germany/munich-starkbierfest.html exists and has the right EN/KO link
ko_stark = 'germany/munich-starkbierfest.html'
en_stark = 'en/germany/munich-starkbierfest.html'

with open(ko_stark, 'r', encoding='utf-8') as f:
    ko_stark_content = f.read()

# Fix the EN link in KO starkbierfest to point to itself, not german-weather
ko_stark_content = ko_stark_content.replace('href="../en/germany/german-weather.html">🇬🇧 EN', 'href="../en/germany/munich-starkbierfest.html">🇬🇧 EN')

with open(ko_stark, 'w', encoding='utf-8') as f:
    f.write(ko_stark_content)

# Create EN version
en_stark_content = ko_stark_content.replace('href="../en/germany/munich-starkbierfest.html">🇬🇧 EN', 'href="../../germany/munich-starkbierfest.html">🇰🇷 KO')
en_stark_content = en_stark_content.replace('lang="ko"', 'lang="en"')
with open(en_stark, 'w', encoding='utf-8') as f:
    f.write(en_stark_content)

# 2. Update Sidebars
sidebar_ko = """          <ul class="sidebar-list" id="postList">
            <li>
              <a href="munich-starkbierfest.html">
                뮌헨 강한 맥주 축제 슈타르크비어페스트 2026
                <span class="sidebar-date">2026.03.27</span>
              </a>
            </li>
            <li>
              <a href="lidl-walnuss-honig-brot-v2.html">
                Lidl 호두꿀빵, 올해도 나를 비껴갔다
                <span class="sidebar-date">2026.03.17</span>
              </a>
            </li>
            <li>
              <a href="german-sick.html">
                독일에서 아프면 각오해야 한다
                <span class="sidebar-date">2026.03.15</span>
              </a>
            </li>
            <li>
              <a href="german-weather.html">
                독일 날씨가 정신병자인 이유 8가지
                <span class="sidebar-date">2026.03.12</span>
              </a>
            </li>
          </ul>"""

sidebar_en = """          <ul class="sidebar-list" id="postList">
            <li>
              <a href="munich-starkbierfest.html">
                Munich Starkbierfest Complete Guide 2026
                <span class="sidebar-date">2026.03.27</span>
              </a>
            </li>
            <li>
              <a href="lidl-walnuss-honig-brot-v2.html">
                Lidl Honey Walnut Bread, missed me again
                <span class="sidebar-date">2026.03.17</span>
              </a>
            </li>
            <li>
              <a href="german-sick.html">
                Be prepared if you get sick in Germany
                <span class="sidebar-date">2026.03.15</span>
              </a>
            </li>
            <li>
              <a href="german-weather.html">
                German weather is crazy — 8 reasons why
                <span class="sidebar-date">2026.03.12</span>
              </a>
            </li>
          </ul>"""

for root, _, files in os.walk('.'):
    if '.git' in root or '.gemini' in root or 'assets' in root: continue
    for f in files:
        if f.endswith('.html') and ('germany' in root):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # replace everything from <ul class="sidebar-... id="postList"> to </ul>
            import re
            is_en = 'en' in path.split(os.sep)
            new_sidebar = sidebar_en if is_en else sidebar_ko
            
            content = re.sub(r'<ul class="sidebar-list" id="postList">.*?</ul>', new_sidebar, content, flags=re.DOTALL)
            
            # Mark the current active one
            filename = os.path.basename(path)
            content = content.replace(f'href="{filename}"', f'href="{filename}" class="current"')
            
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)

# 3. Update recent posts on index.html and en/index.html
recent_ko = """      <div class="recent-grid">

        <a href="./germany/munich-starkbierfest.html" class="post-card">
          <div class="post-num" aria-hidden="true">01</div>
          <div>
            <p class="post-meta">🇩🇪 Germany · Mar 2026</p>
            <p class="post-title">뮌헨 강한 맥주 축제 슈타르크비어페스트 2026</p>
            <span class="post-tag">#뮌헨맥주축제</span>
          </div>
        </a>

        <a href="./germany/lidl-walnuss-honig-brot-v2.html" class="post-card">
          <div class="post-num" aria-hidden="true">02</div>
          <div>
            <p class="post-meta">🇩🇪 Germany · Mar 2026</p>
            <p class="post-title">Lidl 호두꿀빵, 올해도 나를 비껴갔다</p>
            <span class="post-tag">#독일생활</span>
          </div>
        </a>

        <a href="./germany/german-sick.html" class="post-card">
          <div class="post-num" aria-hidden="true">03</div>
          <div>
            <p class="post-meta">🇩🇪 Germany · Mar 2026</p>
            <p class="post-title">독일에서 아프면 각오해야 한다</p>
            <span class="post-tag">#병원</span>
          </div>
        </a>

        <a href="./germany/german-weather.html" class="post-card">
          <div class="post-num" aria-hidden="true">04</div>
          <div>
            <p class="post-meta">🇩🇪 Germany · Mar 2026</p>
            <p class="post-title">독일 날씨가 미쳤다 — 정신병자인 이유 8가지</p>
            <span class="post-tag">#날씨</span>
          </div>
        </a>

      </div>"""

recent_en = """      <div class="recent-grid">

        <a href="./germany/munich-starkbierfest.html" class="post-card">
          <div class="post-num" aria-hidden="true">01</div>
          <div>
            <p class="post-meta">🇩🇪 Germany · Mar 2026</p>
            <p class="post-title">Munich Starkbierfest Complete Guide 2026</p>
            <span class="post-tag">#뮌헨맥주축제</span>
          </div>
        </a>

        <a href="./germany/lidl-walnuss-honig-brot-v2.html" class="post-card">
          <div class="post-num" aria-hidden="true">02</div>
          <div>
            <p class="post-meta">🇩🇪 Germany · Mar 2026</p>
            <p class="post-title">Lidl Honey Walnut Bread, missed me again</p>
            <span class="post-tag">#독일생활</span>
          </div>
        </a>

        <a href="./germany/german-sick.html" class="post-card">
          <div class="post-num" aria-hidden="true">03</div>
          <div>
            <p class="post-meta">🇩🇪 Germany · Mar 2026</p>
            <p class="post-title">Be prepared if you get sick in Germany</p>
            <span class="post-tag">#병원</span>
          </div>
        </a>

        <a href="./germany/german-weather.html" class="post-card">
          <div class="post-num" aria-hidden="true">04</div>
          <div>
            <p class="post-meta">🇩🇪 Germany · Mar 2026</p>
            <p class="post-title">German weather is crazy — 8 reasons why</p>
            <span class="post-tag">#날씨</span>
          </div>
        </a>

      </div>"""

for f in ['index.html', 'en/index.html']:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    new_recent = recent_en if f.startswith('en') else recent_ko
    content = re.sub(r'<div class="recent-grid">.*?</div>\s*</section>', new_recent + '\n    </section>', content, flags=re.DOTALL)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Sidebars and recent posts successfully updated.")
