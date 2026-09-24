import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# 1. Hide the right column when isBulk is true
# Find the left column
text = text.replace('<div className="col-md-8">', '<div className={`col-md-${isBulk ? 12 : 8}`}>')
# Find the right column
text = text.replace('<div className="col-md-4">', '<div className={`col-md-4 ${isBulk ? "d-none" : ""}`}>')

# 2. Extract bulk-mode-container from URL tab
bulk_regex = r'(<div id="bulk-mode-container".*?</div>\s*</div>\s*</div>)' # wait, need to be careful with regex for nested divs
