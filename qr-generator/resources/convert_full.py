import re

with open('../qr-generator/resources/views/qr/index.blade.php', 'r') as f:
    html = f.read()

# Remove blade
html = re.sub(r'@extends\([^)]+\)', '', html)
html = re.sub(r'@section\([^)]+\)', '', html)
html = re.sub(r'@endsection', '', html)

# Convert class to className
html = re.sub(r'\bclass=', 'className=', html)

# Convert for to htmlFor
html = re.sub(r'\bfor=', 'htmlFor=', html)

# Fix comments
html = re.sub(r'<!--(.*?)-->', r'{/* \1 */}', html, flags=re.DOTALL)

# Self close tags
html = re.sub(r'(<input[^>]+?)(?<!/)>', r'\1 />', html)
html = re.sub(r'(<img[^>]+?)(?<!/)>', r'\1 />', html)
html = re.sub(r'(<hr[^>]*?)(?<!/)>', r'\1 />', html)
html = re.sub(r'(<br[^>]*?)(?<!/)>', r'\1 />', html)

# Strip inline styles for now to prevent JSX errors, we can add them back later or they might just be fine
# Actually, let's just regex replace known styles
styles = {
    'style="display: none;"': "style={{ display: 'none' }}",
    'style="display: flex; align-items: center; justify-content: center; background: #f8fafc; border-radius: 0.5rem; margin-bottom: 1rem; border: 1px dashed var(--border-color);"': "style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f8fafc', borderRadius: '0.5rem', marginBottom: '1rem', border: '1px dashed var(--border-color)' }}",
    'style="position: sticky; top: 2rem; border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05);"': "style={{ position: 'sticky', top: '2rem', borderRadius: '0.5rem', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}",
    'style="border-bottom: 1px solid var(--border-color);"': "style={{ borderBottom: '1px solid var(--border-color)' }}",
    'style="height: 50px;"': "style={{ height: '50px' }}",
    'style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 1050; align-items: center; justify-content: center;"': "style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', background: 'rgba(0,0,0,0.6)', zIndex: 1050, alignItems: 'center', justifyContent: 'center' }}",
    'style="width: 90%; max-width: 800px; max-height: 90vh; overflow-y: auto; position: relative;"': "style={{ width: '90%', maxWidth: '800px', maxHeight: '90vh', overflowY: 'auto', position: 'relative' }}",
    'style="position: absolute; top: 1rem; right: 1rem;"': "style={{ position: 'absolute', top: '1rem', right: '1rem' }}",
    'style="max-height: 300px;"': "style={{ maxHeight: '300px' }}",
    'style="width: 0%"': "style={{ width: '0%' }}",
    'style="max-width: 150px;"': "style={{ maxWidth: '150px' }}",
    'style="font-size: 0.9rem;"': "style={{ fontSize: '0.9rem' }}",
    'style="font-size: 0.875rem;"': "style={{ fontSize: '0.875rem' }}",
    'style="max-width: 250px;"': "style={{ maxWidth: '250px' }}"
}

for k, v in styles.items():
    html = html.replace(k, v)

# Fix onClick handlers
def fix_onclick(match):
    code = match.group(1).replace('"', "'")
    return f"onClick={{() => {{ {code} }}}}"

html = re.sub(r'onclick="(.*?)"', fix_onclick, html)

# Add basic React component wrapper
out = f"""'use client';
import React, {{ useState }} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function Page() {{
    const [activeTab, setActiveTab] = useState('url');
    const [isBulk, setIsBulk] = useState(false);
    
    // We will port the logic here later

    return (
        <div className="container mt-4 mb-5">
            {html}
        </div>
    );
}}
"""

with open('src/app/page.js', 'w') as f:
    f.write(out)

print("Converted successfully")
