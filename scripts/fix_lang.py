import re, glob

files = glob.glob('germany/*.html') + ['index.html', 'en/index.html', 'en/germany/index.html']
count = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        c = fh.read()
    new = re.sub(r'<html\s+lang="en"', '<html lang="ko"', c, count=1)
    if new != c:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new)
        count += 1
        print(f'Fixed: {f}')
print(f'lang attribute fixed in {count} files')
