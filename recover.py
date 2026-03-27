import os

with open('en/germany/munich-starkbierfest.html', 'r', encoding='utf-8') as f:
    ko_content = f.read()

# restore lang and KO->EN mapping
ko_content = ko_content.replace('lang="en"', 'lang="ko"')
ko_content = ko_content.replace('href="../../germany/munich-starkbierfest.html">🇰🇷 KO', 'href="../en/germany/munich-starkbierfest.html">🇬🇧 EN')

# fix the toc nav
ko_content = ko_content.replace('<nav class="toc">', '<div class="toc">')
ko_content = ko_content.replace('    </ol>\n  </nav>', '    </ol>\n  </div>')

with open('germany/munich-starkbierfest.html', 'w', encoding='utf-8') as f:
    f.write(ko_content)

# fix the toc in the EN version too
with open('en/germany/munich-starkbierfest.html', 'r', encoding='utf-8') as f:
    en_content = f.read()
en_content = en_content.replace('<nav class="toc">', '<div class="toc">')
en_content = en_content.replace('    </ol>\n  </nav>', '    </ol>\n  </div>')
with open('en/germany/munich-starkbierfest.html', 'w', encoding='utf-8') as f:
    f.write(en_content)

print('Success!')
