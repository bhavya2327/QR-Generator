import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# Fix Accordion Toggles
# 1. Enter Content doesn't toggle
# 2. Set Colors
text = text.replace(
    '<div className="bg-white p-3 rounded mb-2 border cursor-pointer font-weight-bold" style={{ cursor: "pointer" }} onClick={() => document.getElementById("colors-section").classList.toggle("d-none")}>',
    '<div className="bg-white p-3 rounded mb-2 border cursor-pointer font-weight-bold" style={{ cursor: "pointer", display: "flex", justifyContent: "space-between" }} onClick={() => document.getElementById("colors-section").classList.toggle("d-none")}>'
)
# Make sure the section has id
text = text.replace('<div className="p-4 bg-white d-none" id="colors-section">', '<div className="p-4 bg-white d-none border-start border-end border-bottom mb-2" id="colors-section">')

# 3. Add Logo
text = text.replace(
    '<div className="bg-white p-3 rounded mb-2 border cursor-pointer font-weight-bold" onClick={() => {}}>',
    '<div className="bg-white p-3 rounded mb-2 border cursor-pointer font-weight-bold" style={{ cursor: "pointer", display: "flex", justifyContent: "space-between" }} onClick={() => document.getElementById("logo-section").classList.toggle("d-none")}>'
)
text = text.replace('<div className="p-4 bg-white d-none" id="logo-section">', '<div className="p-4 bg-white d-none border-start border-end border-bottom mb-2" id="logo-section">')

# 4. Customize Design
text = text.replace(
    '<div className="bg-white p-3 rounded mb-2 border cursor-pointer font-weight-bold" onClick={() => {}}>',
    '<div className="bg-white p-3 rounded mb-2 border cursor-pointer font-weight-bold" style={{ cursor: "pointer", display: "flex", justifyContent: "space-between" }} onClick={() => document.getElementById("design-section").classList.toggle("d-none")}>'
)
text = text.replace('<div className="p-4 bg-white d-none" id="design-section">', '<div className="p-4 bg-white d-none border-start border-end border-bottom mb-2" id="design-section">')

# The user screenshot showed the "Bulk Mode" toggle inside "1. Enter Content" correctly, but maybe we should ensure it looks good
text = text.replace('Bulk Mode <input type="checkbox"', 'Bulk Mode &nbsp;<input type="checkbox"')

with open('src/app/page.js', 'w') as f:
    f.write(text)

print("UI Fixed")
