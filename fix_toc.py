import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix the broken main nav if it exists
    # The main nav ends right before <div class="page-wrap">
    content = re.sub(r'    </ul>\n  </div>\n\n  <div class="page-wrap">', r'    </ul>\n  </nav>\n\n  <div class="page-wrap">', content)

    # Change <nav class="toc"> to <div class="toc">
    content = content.replace('<nav class="toc">', '<div class="toc">')
    
    # Change the specific </nav> of toc to </div>
    # The toc ends before <!-- INTRO --> or <section id="intro">
    content = re.sub(r'    </ol>\n  </nav>', r'    </ol>\n  </div>', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('germany/munich-starkbierfest.html')
fix_file('en/germany/munich-starkbierfest.html')
