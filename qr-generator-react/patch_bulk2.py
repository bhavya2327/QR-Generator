import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# Replace the specific bulk progress container
old_progress = """                <div id="bulk-progress-container"  className="mt-4">
                    <p className="mb-2 text-center font-weight-bold">Generating QR Codes...</p>
                    <div className="progress-bar-bg">
                        <div className="progress-bar-fill" id="bulk-progress-fill" style={{ width: '0%' }}></div>
                    </div>
                    <p className="text-center mt-2 text-muted" style={{ fontSize: '0.875rem' }} id="bulk-progress-text">0% (0 / 0)</p>
                </div>"""

new_progress = """                <div id="bulk-progress-container" className={isBulk && bulkStage !== 'idle' ? "mt-4" : "d-none"}>
                    <p className="mb-2 text-center font-weight-bold">Generating QR Codes...</p>
                    <div className="progress-bar-bg">
                        <div className="progress-bar-fill" id="bulk-progress-fill" style={{ width: `${bulkProgress}%` }}></div>
                    </div>
                    <p className="text-center mt-2 text-muted" style={{ fontSize: '0.875rem' }} id="bulk-progress-text">{bulkProgress}% ({bulkRecords.filter(r => r.status === 'Valid').length} / {bulkRecords.filter(r => r.status === 'Valid').length})</p>
                </div>"""

text = text.replace(old_progress, new_progress)

with open('src/app/page.js', 'w') as f:
    f.write(text)

