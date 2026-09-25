import re

with open("src/app/page.js", "r") as f:
    text = f.read()
    
# Extract only the JSX portion (roughly)
jsx_start = text.find("return (")
if jsx_start != -1:
    text = text[jsx_start:]

lines = text.split("\n")
stack = []

for i, line in enumerate(lines):
    # Find all <div... and </div
    opens = re.findall(r'<div[\s>]', line)
    closes = re.findall(r'</div>', line)
    
    for _ in opens:
        stack.append(i + 1)
    for _ in closes:
        if stack:
            stack.pop()
        else:
            print(f"Extra closing div on line {i+1}: {line.strip()}")

print(f"Unclosed divs: {len(stack)}")
for line_num in stack:
    print(f"Opened on line: {line_num} (or offset depending on text slice)")
