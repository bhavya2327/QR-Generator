import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# 1. Add states
state_addition = """
    const [isContentOpen, setIsContentOpen] = useState(true);
    const [isColorOpen, setIsColorOpen] = useState(false);
    const [isLogoOpen, setIsLogoOpen] = useState(false);
    const [isDesignOpen, setIsDesignOpen] = useState(false);
"""
text = text.replace(
    "const [bodyShape, setBodyShape] = useState('square');",
    "const [bodyShape, setBodyShape] = useState('square');" + state_addition
)


# 2. Update Content Section
content_header_old = """onClick={() => { document.getElementById('content-section').classList.toggle('d-none') }}"""
content_header_new = """onClick={() => setIsContentOpen(!isContentOpen)}"""
text = text.replace(content_header_old, content_header_new)

content_icon_old = """<i className="fas fa-chevron-down text-muted"></i>"""
content_icon_new = """<i className={`fas ${isContentOpen ? 'fa-chevron-up' : 'fa-chevron-down'} text-muted`}></i>"""
text = text.replace(content_icon_old, content_icon_new, 1)

content_body_old = """<div className="p-4 bg-white" id="content-section">"""
content_body_new = """<div className={`p-4 bg-white ${isContentOpen ? '' : 'd-none'}`} id="content-section">"""
text = text.replace(content_body_old, content_body_new)


# 3. Update Color Section
color_header_old = """onClick={() => { document.getElementById('color-section').classList.toggle('d-none') }}"""
color_header_new = """onClick={() => setIsColorOpen(!isColorOpen)}"""
text = text.replace(color_header_old, color_header_new)

color_icon_old = """<i className="fas fa-chevron-down text-muted"></i>"""
color_icon_new = """<i className={`fas ${isColorOpen ? 'fa-chevron-up' : 'fa-chevron-down'} text-muted`}></i>"""
text = text.replace(color_icon_old, color_icon_new, 1)

color_body_old = """<div className="p-4 bg-white d-none" id="color-section">"""
color_body_new = """<div className={`p-4 bg-white ${isColorOpen ? '' : 'd-none'}`} id="color-section">"""
text = text.replace(color_body_old, color_body_new)


# 4. Update Logo Section
logo_header_old = """onClick={() => { document.getElementById('logo-section').classList.toggle('d-none') }}"""
logo_header_new = """onClick={() => setIsLogoOpen(!isLogoOpen)}"""
text = text.replace(logo_header_old, logo_header_new)

logo_icon_old = """<i className="fas fa-chevron-down text-muted"></i>"""
logo_icon_new = """<i className={`fas ${isLogoOpen ? 'fa-chevron-up' : 'fa-chevron-down'} text-muted`}></i>"""
text = text.replace(logo_icon_old, logo_icon_new, 1)

logo_body_old = """<div className="p-4 bg-white d-none border-start border-end border-bottom mb-2" id="logo-section">"""
logo_body_new = """<div className={`p-4 bg-white ${isLogoOpen ? '' : 'd-none'} border-start border-end border-bottom mb-2`} id="logo-section">"""
text = text.replace(logo_body_old, logo_body_new)


# 5. Update Design Section
design_header_old = """onClick={() => { document.getElementById('design-section').classList.toggle('d-none') }}"""
design_header_new = """onClick={() => setIsDesignOpen(!isDesignOpen)}"""
text = text.replace(design_header_old, design_header_new)

design_icon_old = """<i className="fas fa-chevron-down text-muted"></i>"""
design_icon_new = """<i className={`fas ${isDesignOpen ? 'fa-chevron-up' : 'fa-chevron-down'} text-muted`}></i>"""
text = text.replace(design_icon_old, design_icon_new, 1)

design_body_old = """<div className="p-4 bg-white d-none border-start border-end border-bottom mb-2" id="design-section">"""
design_body_new = """<div className={`p-4 bg-white ${isDesignOpen ? '' : 'd-none'} border-start border-end border-bottom mb-2`} id="design-section">"""
text = text.replace(design_body_old, design_body_new)


with open('src/app/page.js', 'w') as f:
    f.write(text)

