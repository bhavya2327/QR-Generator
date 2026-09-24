import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# 1. Wire the toggle switch to React state
text = text.replace(
    '<input className="form-check-input mt-0" type="checkbox" id="bulk-toggle-switch"  />',
    '<input className="form-check-input mt-0" type="checkbox" id="bulk-toggle-switch" checked={isBulk} onChange={(e) => setIsBulk(e.target.checked)} />'
)

# 2. Hide single-mode-container and show bulk-mode-container based on state
text = text.replace('<div id="single-mode-container">', '<div id="single-mode-container" className={isBulk ? "d-none" : ""}>')
text = text.replace('<div id="bulk-mode-container" style={{ display: \'none\' }}>', '<div id="bulk-mode-container" className={isBulk ? "" : "d-none"}>')

# 3. Wire the browse button to trigger the file input
text = text.replace(
    '<button className="btn btn-sm btn-outline" id="browse-btn">Browse Files</button>',
    '<button className="btn btn-sm btn-outline" id="browse-btn" onClick={() => document.getElementById("csv-file").click()}>Browse Files</button>'
)

# 4. Bind the file input to onFileUpload
text = text.replace(
    '<input type="file" id="csv-file" accept=".csv" style={{ display: \'none\' }} />',
    '<input type="file" id="csv-file" accept=".csv" style={{ display: \'none\' }} onChange={onFileUpload} />'
)

# 5. Hide the right hand preview stuff when in bulk mode
text = text.replace(
    '<div id="qr-preview-box"',
    '<div id="qr-preview-box" className={isBulk ? "d-none" : ""}'
)
text = text.replace(
    '<button className="btn btn-success btn-lg w-100 font-weight-bold" id="main-generate-btn">Create QR Code</button>',
    '<button className={`btn btn-success btn-lg w-100 font-weight-bold ${isBulk ? "d-none" : ""}`} id="main-generate-btn">Create QR Code</button>'
)
text = text.replace(
    '<div id="download-actions" className="mt-3">',
    '<div id="download-actions" className={`mt-3 ${isBulk ? "d-none" : ""}`}>'
)

with open('src/app/page.js', 'w') as f:
    f.write(text)

print("Bulk UI wired")
