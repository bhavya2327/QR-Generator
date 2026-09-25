with open('src/app/page.js', 'r') as f:
    text = f.read()

# 1. Update columns
text = text.replace('<div className="col-md-8">', '<div className={`col-md-${isBulk ? 12 : 8}`}>')
text = text.replace('<div className="col-md-4">', '<div className={`col-md-4 ${isBulk ? "d-none" : ""}`}>')

# 2. Extract bulk container
import re
match = re.search(r'(<div id="bulk-mode-container".*?<div id="bulk-error-message"[^>]*></div>\s*</div>)', text, re.DOTALL)
bulk_code = match.group(1)

text = text.replace(bulk_code, "")

# 3. Remove the inner single-mode-container from content-url
text = text.replace('<div id="single-mode-container" className={isBulk ? "d-none" : ""}>', '')
# The closing tag for single-mode-container was just before the bulk-mode-container we extracted.
# Since we extracted bulk-mode-container, the structure in content-url is now:
# <div id="content-url" ...>
#    <form> ... </form>
#    </div>
# </div>
# We need to remove that extra </div>
text = text.replace('</form>\n                        </div>\n\n                        \n                    </div>', '</form>\n                    </div>')

# 4. Wrap ALL content-* inside a new single-mode-container, and append bulk-mode-container
# The content section starts at: <div className={`p-4 bg-transparent-glass ${isContentOpen ? '' : 'd-none'}`} id="content-section">
# We want to insert <div className={isBulk ? "d-none" : ""}> right after it.
start_str = """<div className={`p-4 bg-transparent-glass ${isContentOpen ? '' : 'd-none'}`} id="content-section">"""
new_start_str = start_str + """\n                    <div className={isBulk ? "d-none" : ""}>"""
text = text.replace(start_str, new_start_str)

# We need to close this new div, and append bulk_code right before the end of content-section
# Let's find the end of content-section. It ends right before:
#             </div>
#         </div>
#         {/*  2. Set Colors  */}
end_str = """                    </div>
                </div>

                {/*  2. Set Colors  */}"""
                
new_end_str = f"""                    </div>
                    {bulk_code}
                </div>

                {{/*  2. Set Colors  */}}"""
text = text.replace(end_str, new_end_str)

with open('src/app/page.js', 'w') as f:
    f.write(text)

