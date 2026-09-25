import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# 1. Hide the native file input again
# Current: <input type="file" id="csv-file" accept=".csv"  onChange={onFileUpload} />
text = re.sub(r'<input type="file" id="csv-file" accept="\.csv"\s*(onChange=\{onFileUpload\})? />', 
              r'<input type="file" id="csv-file" accept=".csv" style={{ display: "none" }} onChange={onFileUpload} />', text)

# Just in case it looks slightly different:
text = text.replace('<input type="file" id="csv-file" accept=".csv"  onChange={onFileUpload} />', 
                    '<input type="file" id="csv-file" accept=".csv" style={{ display: "none" }} onChange={onFileUpload} />')
text = text.replace('<input type="file" id="csv-file" accept=".csv" onChange={onFileUpload} />', 
                    '<input type="file" id="csv-file" accept=".csv" style={{ display: "none" }} onChange={onFileUpload} />')

# 2. Hide the bulk progress indicator when idle
# The JSX for the progress container starts near <div id="bulk-progress-container"
# We need to wrap it in a condition. Let's find it.

progress_old = """                <div id="bulk-progress-container" className="mt-3">
                    <div className="text-center mb-2 small text-muted">Generating QR Codes...</div>
                    <div className="progress-bar-bg">
                        <div className="progress-bar-fill" style={{ width: `${bulkProgress}%` }}></div>
                    </div>
                    <div className="text-center mt-1" style={{ fontSize: '0.75rem', color: 'var(--secondary-color)' }}>
                        {bulkProgress}% ({bulkRecords.filter(r => r.status === 'Valid').length} / {bulkRecords.filter(r => r.status === 'Valid').length})
                    </div>
                </div>"""

progress_new = """                {bulkStage !== 'idle' && (
                    <div id="bulk-progress-container" className="mt-3">
                        <div className="text-center mb-2 small text-muted">Generating QR Codes...</div>
                        <div className="progress-bar-bg">
                            <div className="progress-bar-fill" style={{ width: `${bulkProgress}%` }}></div>
                        </div>
                        <div className="text-center mt-1" style={{ fontSize: '0.75rem', color: 'var(--secondary-color)' }}>
                            {bulkProgress}% ({bulkRecords.filter(r => r.status === 'Valid').length} / {bulkRecords.filter(r => r.status === 'Valid').length})
                        </div>
                    </div>
                )}"""

text = text.replace(progress_old, progress_new)

with open('src/app/page.js', 'w') as f:
    f.write(text)
