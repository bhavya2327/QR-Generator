import re
with open('src/app/globals.css', 'r') as f:
    text = f.read()

# Replace the card override
old_card = """.card {
    background-color: transparent !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}"""

new_card = """.card {
    background-color: rgba(255, 255, 255, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    color: #1e1e2f;
}"""

text = text.replace(old_card, new_card)

# also fix .text-muted
text = text.replace("color: #cbd5e1 !important;", "color: #64748b !important;")

with open('src/app/globals.css', 'w') as f:
    f.write(text)
