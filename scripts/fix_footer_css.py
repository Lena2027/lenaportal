"""
Ensures .footer-links CSS is present in any file that has footer-links HTML.
"""
import glob, re

FOOTER_CSS = """
    .footer-links { display: flex; gap: 16px; }
    .footer-links a {
      font-size: 12px; font-weight: 700; color: #999;
      text-decoration: none; font-family: 'Nunito', sans-serif;
    }
    .footer-links a:hover { color: var(--pink); }"""

files = glob.glob('**/*.html', recursive=True)
count = 0
for f in files:
    with open(f,'r',encoding='utf-8') as fh: c=fh.read()
    if 'class="footer-links"' in c and '.footer-links' not in c:
        # Add CSS before closing </style>
        new = re.sub(r'(\s*</style>)', FOOTER_CSS + r'\1', c, count=1)
        if new != c:
            with open(f,'w',encoding='utf-8') as fh: fh.write(new)
            count += 1
            print(f'Added footer-links CSS: {f}')
print(f'Fixed {count} files')
