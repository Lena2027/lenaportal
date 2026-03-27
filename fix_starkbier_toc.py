import os

paths = [
    'germany/munich-starkbierfest.html',
    'en/germany/munich-starkbierfest.html'
]

for path in paths:
    # Read the file
    with open(path, 'rb') as f:
        raw = f.read()

    # Determine encoding and decode
    if raw.startswith(b'\xff\xfe'):
        content = raw.decode('utf-16le')
    else:
        content = raw.decode('utf-8')
    
    # In germany/munich-starkbierfest.html, if the main nav is broken:
    # It might look like:
    # </ul>
    # </div>
    # 
    # <div class="page-wrap">
    content = content.replace('    </ul>\r\n  </div>\r\n\r\n  <div class="page-wrap">', '    </ul>\n  </nav>\n\n  <div class="page-wrap">')
    content = content.replace('    </ul>\n  </div>\n\n  <div class="page-wrap">', '    </ul>\n  </nav>\n\n  <div class="page-wrap">')
    
    # Fix the <nav class="toc"> issue
    content = content.replace('<nav class="toc">', '<div class="toc">')
    
    # Fix the </nav> for toc
    content = content.replace('    </ol>\r\n  </nav>\r\n', '    </ol>\n  </div>\n')
    content = content.replace('    </ol>\n  </nav>\n', '    </ol>\n  </div>\n')

    # Save as utf-8
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixed encoding and TOC tags for both files.")
