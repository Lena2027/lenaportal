import os
import re
from datetime import datetime

PUBLISH_DIR = 'germany'
EN_PUBLISH_DIR = 'en/germany'
ROOT_INDEX = 'index.html'
EN_ROOT_INDEX = 'en/index.html'

def get_posts(directory):
    posts = []
    if not os.path.exists(directory):
        return posts
        
    for filename in os.listdir(directory):
        if not filename.endswith('.html') or filename == 'index.html':
            continue
        
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        title_match = re.search(r'<meta property="og:title" content="(.*?)">', content)
        if not title_match:
            title_match = re.search(r'<title>(.*?)</title>', content)
        title = title_match.group(1).split('|')[0].strip() if title_match else filename

        date_match = re.search(r'<meta property="article:published_time" content="(.*?)">', content)
        if not date_match:
            date_match = re.search(r'"datePublished":\s*"(.*?)"', content)
        
        date_str = date_match.group(1) if date_match else '2000-01-01'
        try:
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00')).replace(tzinfo=None)
        except:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                date_obj = datetime.min
        
        tag_match = re.search(r'<span class="post-tag">(.*?)</span>', content)
        if not tag_match:
            tag_match = re.search(r'<a href="#" class="tag">(.*?)</a>', content)
        tag = tag_match.group(1) if tag_match else '#블로그'
        tag = tag.split()[0] # take the first word if multiple tags

        posts.append({
            'filename': filename,
            'title': title,
            'date': date_obj,
            'date_str': date_obj.strftime('%Y.%m.%d'),
            'month_str': date_obj.strftime('%b %Y'),
            'tag': tag
        })
    
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

def generate_sidebar_html(posts):
    html = '          <ul class="sidebar-list" id="postList">\n'
    for post in posts:
        html += f'''            <li>
              <a href="{post['filename']}">
                {post['title']}
                <span class="sidebar-date">{post['date_str']}</span>
              </a>
            </li>\n'''
    html += '          </ul>'
    return html

def update_sidebars(directory, posts):
    sidebar_html = generate_sidebar_html(posts)
    for filename in os.listdir(directory):
        if not filename.endswith('.html'):
            continue
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = re.sub(r'<ul class="sidebar-list" id="postList">.*?</ul>', sidebar_html, content, flags=re.DOTALL)
        
        content = content.replace('class="current"', '')
        
        target_filename = posts[0]['filename'] if filename == 'index.html' else filename
        content = content.replace(f'href="{target_filename}"', f'href="{target_filename}" class="current"')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

def update_recent_posts(index_file, posts, is_en=False):
    html = '      <div class="recent-grid">\n\n'
    
    for i, post in enumerate(posts[:4]):
        num = f"0{i+1}"
        html += f'''        <a href="./germany/{post['filename']}" class="post-card">
          <div class="post-num" aria-hidden="true">{num}</div>
          <div>
            <p class="post-meta">🇩🇪 Germany · {post['month_str']}</p>
            <p class="post-title">{post['title']}</p>
            <span class="post-tag">{post['tag']}</span>
          </div>
        </a>\n\n'''
    html += '      </div>'

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(r'<div class="recent-grid">.*?</div>\s*</section>', html + '\n    </section>', content, flags=re.DOTALL)
    
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)

def update_category_index(directory, posts):
    index_path = os.path.join(directory, 'index.html')
    if not os.path.exists(index_path): return

    html = ""
    for post in posts:
        html += f'''      <a href="./{post['filename']}" class="post-card">
        <div class="post-meta">{post['date_str']}</div>
        <h3 class="post-title">{post['title']}</h3>
        <span class="post-tag">{post['tag']}</span>
      </a>\n'''

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 정규식을 이용해 주석 사이의 내용을 덮어씁니다.
    content = re.sub(
        r'<!-- POSTS -->.*?<!-- /POSTS -->',
        f'<!-- POSTS -->\n{html}      <!-- /POSTS -->',
        content,
        flags=re.DOTALL
    )

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    ko_posts = get_posts(PUBLISH_DIR)
    update_category_index(PUBLISH_DIR, ko_posts)
    update_sidebars(PUBLISH_DIR, ko_posts)
    update_recent_posts(ROOT_INDEX, ko_posts, False)

    if os.path.exists(EN_PUBLISH_DIR):
        en_posts = get_posts(EN_PUBLISH_DIR)
        update_category_index(EN_PUBLISH_DIR, en_posts)
        update_sidebars(EN_PUBLISH_DIR, en_posts)
        update_recent_posts(EN_ROOT_INDEX, en_posts, True)

    print("Blog pages successfully updated with the latest posts!")
