import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# 1. Update columns for isBulk
text = text.replace('<div className="col-md-8">', '<div className={`col-md-${isBulk ? 12 : 8}`}>')
text = text.replace('<div className="col-md-4">', '<div className={`col-md-4 ${isBulk ? "d-none" : ""}`}>')

# 2. Extract bulk-mode-container
bulk_container_match = re.search(r'(<div id="bulk-mode-container".*?<div id="bulk-error-message".*?</div>\s*</div>)', text, re.DOTALL)
if not bulk_container_match:
    print("Could not find bulk container!")
    exit(1)

bulk_container_code = bulk_container_match.group(1)

# Remove it from its current location
text = text.replace(bulk_container_code, '')

# 3. We also have a `<div id="single-mode-container"` that we should probably just remove or rename, because we want to wrap ALL content-* in it.
# Actually, `content-url` has:
# <div id="content-url" ...>
#     <div id="single-mode-container" className={isBulk ? "d-none" : ""}>
#         <form id="single-qr-form"> ... </form>
#     </div>
# </div>
# Let's remove `<div id="single-mode-container" className={isBulk ? "d-none" : ""}>` and its closing `</div>` from `content-url`.
text = text.replace('<div id="single-mode-container" className={isBulk ? "d-none" : ""}>', '')
# The closing div is right before where bulk-mode-container was.
text = re.sub(r'</form>\s*</div>\s*</div>', '</form>\n                    </div>', text) # careful here

# Let's just do it manually with simple string splits to be extremely safe.
