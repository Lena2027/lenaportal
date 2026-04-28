"""
Adds Privacy Policy + About links to all page footers.
Run from repo root: python3 scripts/add_footer_links.py
"""
import re, glob, os

# Files and their relative path prefix for About/Privacy
FILE_GROUPS = [
    # (glob_pattern, about_path, privacy_path)
    (['index.html'],                            './about/index.html',      './privacy-policy.html'),
    (glob.glob('germany/*.html'),               '../about/index.html',     '../privacy-policy.html'),
    (['en/index.html'],                         './about/index.html',      './privacy-policy.html'),
    (['en/germany/index.html'],                 '../../about/index.html',  '../../privacy-policy.html'),
]

FOOTER_LINKS_PATTERN = re.compile(
    r'<div class="footer-links">.*?</div>',
    re.DOTALL
)

count = 0
for group_files, about_path, privacy_path in FILE_GROUPS:
    for filepath in group_files:
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if footer-links already present
        if 'footer-links' in content:
            print(f'Already has footer-links: {filepath}')
            continue

        # Find </footer> and insert footer-links just before closing tag
        FOOTER_CLOSE = re.compile(r'(\s*</footer>)', re.MULTILINE)
        footer_links_html = f'''
    <div class="footer-links">
      <a href="{about_path}">About</a>
      <a href="{privacy_path}">Privacy Policy</a>
    </div>'''

        new_content = FOOTER_CLOSE.sub(footer_links_html + r'\1', content, count=1)

        if new_content == content:
            print(f'No </footer> found: {filepath}')
            continue

        # Ensure footer-links CSS is present
        if '.footer-links' not in new_content:
            # Add CSS before </style> in the <head>
            footer_links_css = """
    .footer-links { display: flex; gap: 16px; }
    .footer-links a {
      font-size: 12px; font-weight: 700; color: #999;
      text-decoration: none; font-family: 'Nunito', sans-serif;
    }
    .footer-links a:hover { color: var(--pink); }"""
            new_content = new_content.replace('  </style>', footer_links_css + '\n  </style>', 1)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f'Updated: {filepath}')

print(f'\nTotal updated: {count} files')
