import re
with open('src/app/globals.css', 'r') as f:
    text = f.read()

# Replace the body rule that has the background image
old_body = """/* Custom overrides for the Neon Blue Theme */
body {
    background-image: url('/background.png');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
    background-color: #0b0c10; /* Fallback dark color */
    color: #ffffff; /* Keep base text readable against dark mode if needed, though cards are white */
}"""

new_body = """/* Custom overrides */
body {
    background-color: #f3e8ff; /* Baby purple color */
    color: #1e1e2f; /* Darker text for light background */
}"""

text = text.replace(old_body, new_body)

# Since the background is now very light, the dark glassmorphism might be too dark.
# But let's leave the glassmorphism or adjust it to be lighter glass?
# Let's adjust glassmorphism to be white-ish glass so it looks good on purple!
old_glass = """.bg-transparent-glass {
    background-color: rgba(15, 23, 42, 0.6) !important;
    backdrop-filter: blur(12px);
    color: #f8fafc;
}"""
new_glass = """.bg-transparent-glass {
    background-color: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(12px);
    color: #1e1e2f;
}"""
text = text.replace(old_glass, new_glass)

old_glass_header = """.bg-transparent-glass-header {
    background-color: rgba(30, 58, 138, 0.5) !important;
    backdrop-filter: blur(12px);
    color: #f8fafc;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}"""
new_glass_header = """.bg-transparent-glass-header {
    background-color: rgba(255, 255, 255, 0.85) !important;
    backdrop-filter: blur(12px);
    color: #1e1e2f;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;
}"""
text = text.replace(old_glass_header, new_glass_header)

old_card = """.card {
    background-color: rgba(15, 23, 42, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f8fafc;
}"""
new_card = """.card {
    background-color: rgba(255, 255, 255, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    color: #1e1e2f;
}"""
text = text.replace(old_card, new_card)

# Fix text colors for inputs and labels that might have been forced to white
text = text.replace("color: #f8fafc !important;", "color: #1e1e2f !important;")
text = text.replace("color: #ffffff !important;", "color: #1e1e2f !important;")
text = text.replace("background-color: rgba(255, 255, 255, 0.1) !important;", "background-color: rgba(255, 255, 255, 0.8) !important;")
text = text.replace("border: 1px solid rgba(255, 255, 255, 0.2) !important;", "border: 1px solid rgba(0, 0, 0, 0.1) !important;")

with open('src/app/globals.css', 'w') as f:
    f.write(text)
