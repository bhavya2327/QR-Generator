import re

with open('src/app/page.js', 'r') as f:
    content = f.read()

# Replace column size
content = content.replace('col-md-${isBulk ? 12 : 8}', 'col-md-${isBulk ? 12 : 7}')

# Replace Enter Content header logic
enter_content_old = r'''<div className="card mb-3 p-0 overflow-hidden">
                <div className="card-header bg-transparent-glass-header d-flex justify-content-between align-items-center p-3 cursor-pointer" style={{ borderBottom: '1px solid var\(--border-color\)', cursor: 'pointer' }} onClick={() => setIsContentOpen\(!isContentOpen\)}>
                    <h5 className="mb-0">1. Enter Content</h5>
                    <div className="d-flex align-items-center gap-3">
                        <div className="form-check form-switch m-0 d-flex align-items-center" onClick={\(e\) => e.stopPropagation\(\)}>
                            <label className="form-check-label me-2 text-muted" htmlFor="bulk-toggle-switch" style={{ fontSize: '0.875rem' }}>Bulk Mode</label>
                            <input className="form-check-input mt-0" type="checkbox" id="bulk-toggle-switch" style={{ cursor: 'pointer', width: '2.5em', height: '1.25em', marginLeft: '0.5rem' }} checked={isBulk} onChange={\(e\) => setIsBulk\(e.target.checked\)} />
                        </div>
                        <i className={`fas \${isContentOpen \? 'fa-chevron-up' : 'fa-chevron-down'} text-muted`}></i>
                    </div>
                </div>
                <div className={`p-4 bg-transparent-glass \${isContentOpen \? '' : 'd-none'}`} id="content-section">'''

enter_content_new = r'''<div className="d-flex justify-content-between align-items-center mb-3 px-2">
                <h5 className="fw-bold mb-0">Enter Content</h5>
                <div className="d-flex align-items-center">
                    <label className="form-check-label me-2 text-muted" htmlFor="bulk-toggle-switch" style={{ fontSize: '0.875rem' }}>Bulk Mode</label>
                    <div className="form-check form-switch m-0 d-flex align-items-center">
                        <input className="form-check-input mt-0" type="checkbox" id="bulk-toggle-switch" style={{ cursor: 'pointer', width: '2.5em', height: '1.25em' }} checked={isBulk} onChange={(e) => setIsBulk(e.target.checked)} />
                    </div>
                </div>
            </div>
            
            <div className="p-4 mb-4" style={{ backgroundColor: '#f4f4f5', borderRadius: '24px' }}>
                <div className={isBulk ? "d-none" : ""}>'''

content = re.sub(enter_content_old, enter_content_new, content)

# Now remove the closing `</div> </div>` of the old card.
# The card closed after `{/* SMS Content Form */}`... no wait, after all the type contents. Let's find where `<div className={isBulk ? "d-none" : ""}>` closes.
# Actually, the easiest way is to use multi_replace_file_content or a robust regex.
with open('src/app/page.js', 'w') as f:
    f.write(content)
