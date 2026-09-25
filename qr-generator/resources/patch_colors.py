import re
with open('src/app/globals.css', 'r') as f:
    text = f.read()

# 1. Darken the card border
text = text.replace("border: 1px solid rgba(255, 255, 255, 0.4) !important;", "border: 1px solid rgba(0, 0, 0, 0.15) !important;")

# 2. Darken the input borders
text = text.replace("border: 1px solid rgba(0, 0, 0, 0.1) !important;", "border: 1px solid rgba(0, 0, 0, 0.2) !important;")

# 3. Darken the accordion header border
text = text.replace("border-bottom: 1px solid rgba(0, 0, 0, 0.05) !important;", "border-bottom: 1px solid rgba(0, 0, 0, 0.15) !important;")

# 4. Change btn-success (Create QR Code) to a beautiful violet/purple
old_btn_success = """.btn-success {
    background: linear-gradient(135deg, #0d6efd, #0043a8) !important;
    border-color: #0d6efd !important;
    box-shadow: 0 4px 15px rgba(13, 110, 253, 0.4);
    transition: all 0.3s ease;
}

.btn-success:hover {
    background: linear-gradient(135deg, #0b5ed7, #003380) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(13, 110, 253, 0.6);
}"""

new_btn_success = """.btn-success {
    background: linear-gradient(135deg, #8b5cf6, #6d28d9) !important;
    border-color: #7c3aed !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    transition: all 0.3s ease;
}

.btn-success:hover {
    background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6);
}"""
text = text.replace(old_btn_success, new_btn_success)

# We also need to change the --primary-color to purple so the active tabs look right!
# It's currently --primary-color: #3b82f6;
text = re.sub(r'--primary-color:\s*#3b82f6;', '--primary-color: #8b5cf6;', text)
text = re.sub(r'--primary-hover:\s*#2563eb;', '--primary-hover: #7c3aed;', text)

with open('src/app/globals.css', 'w') as f:
    f.write(text)
