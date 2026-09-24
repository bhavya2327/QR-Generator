import re
with open('src/app/globals.css', 'r') as f:
    text = f.read()

# Remove the first body block
text = re.sub(r'body\s*{[^}]*background-color:\s*var\(--bg-color\);[^}]*}', '', text, flags=re.DOTALL)

with open('src/app/globals.css', 'w') as f:
    f.write(text)
