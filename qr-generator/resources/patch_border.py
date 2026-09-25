import re
with open('src/app/globals.css', 'r') as f:
    text = f.read()

# Change border-color to a darker grey
text = re.sub(r'--border-color:\s*#e2e8f0;', '--border-color: #cbd5e1;', text)

with open('src/app/globals.css', 'w') as f:
    f.write(text)
