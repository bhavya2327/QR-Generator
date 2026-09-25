text = open('src/app/page.js').read()
with open('src/app/page.js', 'w') as f:
    f.write("'use client';\n" + text)
