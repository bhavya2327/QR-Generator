import re

code = open('src/app/page.js').read()

# Add import
code = re.sub(r'import QRCodePreview from \'../components/QRCodePreview\';', 
              'import QRCodePreview from \'../components/QRCodePreview\';\nimport { handleSingleDownload, processBulkCSV } from \'../utils/qrUtils\';', 
              code)

# Wire single downloads
code = code.replace(
    '<button className="btn btn-primary flex-grow-1" id="download-single-png">Download PNG</button>',
    '<button className="btn btn-primary flex-grow-1" onClick={() => handleSingleDownload("png", getQrData(), fgColor, bgColor, styleShape, null)}>Download PNG</button>'
)

code = code.replace(
    '<button className="btn btn-secondary flex-grow-1" id="download-single-svg">Download SVG</button>',
    '<button className="btn btn-secondary flex-grow-1" onClick={() => handleSingleDownload("svg", getQrData(), fgColor, bgColor, styleShape, null)}>Download SVG</button>'
)

code = code.replace('<div id="download-actions" className="mt-3">', '<div id="download-actions" className="mt-3" style={{display: "block"}}>')
# Let's just make the download buttons always visible for now
code = code.replace('<div id="download-actions" className="mt-3" style={{ display: \'none\' }}>', '<div id="download-actions" className="mt-3">')

# Bulk UI is more complex, so we'll just implement the file input hook
bulk_state = """
    const [isBulkProcessing, setIsBulkProcessing] = useState(false);
    const [bulkProgress, setBulkProgress] = useState(0);
    const [bulkText, setBulkText] = useState('');

    const onFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        setIsBulkProcessing(true);
        try {
            await processBulkCSV(file, fgColor, bgColor, styleShape, null, (pct, curr, tot) => {
                setBulkProgress(pct);
                setBulkText(`${pct}% (${curr} / ${tot})`);
            });
            alert('Bulk ZIP generated successfully!');
        } catch(e) {
            alert('Failed to process bulk CSV.');
        }
        setIsBulkProcessing(false);
    };
"""

code = code.replace('// We will port the logic here later', bulk_state)

# Bind the file upload to the CSV input
code = code.replace(
    '<input type="file" id="csv_file" name="csv_file" className="form-control" accept=".csv" required />',
    '<input type="file" id="csv_file" name="csv_file" className="form-control" accept=".csv" required onChange={onFileUpload} />'
)

with open('src/app/page.js', 'w') as f:
    f.write(code)

print("done")
