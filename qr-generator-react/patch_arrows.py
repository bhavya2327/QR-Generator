import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

text = text.replace(
    '2. Set Colors\n                    </div>',
    '2. Set Colors\n                        <i className="fas fa-chevron-down"></i>\n                    </div>'
)

text = text.replace(
    '3. Add Logo Image\n                    </div>',
    '3. Add Logo Image\n                        <i className="fas fa-chevron-down"></i>\n                    </div>'
)

text = text.replace(
    '<h5 className="mb-0">4. Customize Design</h5>\n                    </div>',
    '<h5 className="mb-0">4. Customize Design</h5>\n                        <i className="fas fa-chevron-down"></i>\n                    </div>'
)

# Wait, 4. Customize Design was an h5? Let's check how it's structured in page.js
