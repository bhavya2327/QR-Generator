import re

html = open('../qr-generator/resources/views/qr/index.blade.php').read()

# Remove blade directives
html = re.sub(r'@extends\([^)]+\)', '', html)
html = re.sub(r'@section\([^)]+\)', '', html)
html = re.sub(r'@endsection', '', html)

# Convert class to className
html = re.sub(r'\bclass=', 'className=', html)

# Convert for to htmlFor
html = re.sub(r'\bfor=', 'htmlFor=', html)

# Self-close inputs, img, br, hr, meta, link
html = re.sub(r'(<input[^>]+?)(?<!/)>', r'\1 />', html)
html = re.sub(r'(<img[^>]+?)(?<!/)>', r'\1 />', html)
html = re.sub(r'(<br[^>]*?)(?<!/)>', r'\1 />', html)
html = re.sub(r'(<hr[^>]*?)(?<!/)>', r'\1 />', html)

# Fix style attribute from style="display: none;" to style={{ display: 'none' }}
# We'll just do a basic replace for the specific ones we know exist
html = html.replace('style="display: none;"', "style={{ display: 'none' }}")
html = html.replace('style="display: flex; align-items: center; justify-content: center; background: #f8fafc; border-radius: 0.5rem; margin-bottom: 1rem; border: 1px dashed var(--border-color);"', "style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f8fafc', borderRadius: '0.5rem', marginBottom: '1rem', border: '1px dashed var(--border-color)' }}")
html = html.replace('style="position: sticky; top: 2rem; border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05);"', "style={{ position: 'sticky', top: '2rem', borderRadius: '0.5rem', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}")
html = html.replace('style="border-bottom: 1px solid var(--border-color);"', "style={{ borderBottom: '1px solid var(--border-color)' }}")
html = html.replace('style="height: 50px;"', "style={{ height: '50px' }}")
html = html.replace('style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 1050; align-items: center; justify-content: center;"', "style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', background: 'rgba(0,0,0,0.6)', zIndex: 1050, alignItems: 'center', justifyContent: 'center' }}")
html = html.replace('style="width: 90%; max-width: 800px; max-height: 90vh; overflow-y: auto; position: relative;"', "style={{ width: '90%', maxWidth: '800px', maxHeight: '90vh', overflowY: 'auto', position: 'relative' }}")
html = html.replace('style="position: absolute; top: 1rem; right: 1rem;"', "style={{ position: 'absolute', top: '1rem', right: '1rem' }}")
html = html.replace('style="max-height: 300px;"', "style={{ maxHeight: '300px' }}")
html = html.replace('style="width: 0%"', "style={{ width: '0%' }}")
html = html.replace('style="max-width: 150px;"', "style={{ maxWidth: '150px' }}")
html = html.replace('style="font-size: 0.9rem;"', "style={{ fontSize: '0.9rem' }}")
html = html.replace('style="font-size: 0.875rem;"', "style={{ fontSize: '0.875rem' }}")

# Handle onclick -> onClick
html = html.replace('onclick="', 'onClick={() => ')

# Output to jsx
out = f"""
'use client';
import React, {{ useState }} from 'react';

export default function Page() {{
    return (
        <main>
            {html}
        </main>
    );
}}
"""
with open('src/app/page.js', 'w') as f:
    f.write(out)

