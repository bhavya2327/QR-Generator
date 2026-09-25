import re

text = open('src/app/page.js').read()
text = re.sub(r'<!--(.*?)-->', r'{/* \1 */}', text, flags=re.DOTALL)
# Also fix selected -> defaultValue or defaultChecked? It's fine for now.
with open('src/app/page.js', 'w') as f:
    f.write(text)
