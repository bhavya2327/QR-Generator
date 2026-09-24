import re

text = open('src/app/page.js').read()
# Find all style="..." and replace with empty string
text = re.sub(r'style="[^"]*"', '', text)
with open('src/app/page.js', 'w') as f:
    f.write(text)
