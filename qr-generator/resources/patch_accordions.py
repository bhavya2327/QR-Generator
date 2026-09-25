import re

with open('src/app/page.js', 'r') as f:
    content = f.read()

# 1. Colors
old_colors = r'''<div className={`card mb-3 p-0 overflow-hidden \${isBulk \? 'd-none' : ''}`}>
                <div className="card-header bg-transparent-glass-header d-flex justify-content-between align-items-center p-3 cursor-pointer" style={{ borderBottom: '1px solid var\(--border-color\)', cursor: 'pointer' }} onClick={() => setIsColorOpen\(!isColorOpen\)}>
                    <h5 className="mb-0">2. Set Colors</h5>
                    <i className={`fas \${isColorOpen \? 'fa-chevron-up' : 'fa-chevron-down'} text-muted`}></i>
                </div>
                <div className={`p-4 bg-transparent-glass \${isColorOpen \? '' : 'd-none'}`} id="color-section">'''
new_colors = r'''<div className={`bg-white rounded-3 mb-3 overflow-hidden \${isBulk ? 'd-none' : ''}`} style={{ borderRadius: '12px' }}>
                <div className="d-flex justify-content-between align-items-center p-3 cursor-pointer" onClick={() => setIsColorOpen(!isColorOpen)}>
                    <h6 className="mb-0 fw-bold text-dark">Select Colors</h6>
                </div>
                <div className={`p-4 \${isColorOpen ? '' : 'd-none'}`} id="color-section">'''
content = re.sub(old_colors, new_colors, content)

# 2. Logo
old_logo = r'''<div className={`card mb-3 p-0 overflow-hidden \${isBulk \? 'd-none' : ''}`}>
                <div className="card-header bg-transparent-glass-header d-flex justify-content-between align-items-center p-3 cursor-pointer" style={{ borderBottom: '1px solid var\(--border-color\)', cursor: 'pointer' }} onClick={() => setIsLogoOpen\(!isLogoOpen\)}>
                    <h5 className="mb-0">3. Add Logo Image</h5>
                    <i className={`fas \${isLogoOpen \? 'fa-chevron-up' : 'fa-chevron-down'} text-muted`}></i>
                </div>
                <div className={`p-4 bg-transparent-glass \${isLogoOpen \? '' : 'd-none'} border-start border-end border-bottom mb-2`} id="logo-section">'''
new_logo = r'''<div className={`bg-white rounded-3 mb-3 overflow-hidden \${isBulk ? 'd-none' : ''}`} style={{ borderRadius: '12px' }}>
                <div className="d-flex justify-content-between align-items-center p-3 cursor-pointer" onClick={() => setIsLogoOpen(!isLogoOpen)}>
                    <h6 className="mb-0 fw-bold text-dark">Add Logo Image</h6>
                </div>
                <div className={`p-4 \${isLogoOpen ? '' : 'd-none'}`} id="logo-section">'''
content = re.sub(old_logo, new_logo, content)

# 3. Design
old_design = r'''<div className={`card mb-3 p-0 overflow-hidden \${isBulk \? 'd-none' : ''}`}>
                <div className="card-header bg-transparent-glass-header d-flex justify-content-between align-items-center p-3 cursor-pointer" style={{ borderBottom: '1px solid var\(--border-color\)', cursor: 'pointer' }} onClick={() => setIsDesignOpen\(!isDesignOpen\)}>
                    <h5 className="mb-0">4. Customize Design</h5>
                    <i className={`fas \${isDesignOpen \? 'fa-chevron-up' : 'fa-chevron-down'} text-muted`}></i>
                </div>
                <div className={`p-4 bg-transparent-glass \${isDesignOpen \? '' : 'd-none'} border-start border-end border-bottom mb-2`} id="design-section">'''
new_design = r'''<div className={`bg-white rounded-3 mb-3 overflow-hidden \${isBulk ? 'd-none' : ''}`} style={{ borderRadius: '12px' }}>
                <div className="d-flex justify-content-between align-items-center p-3 cursor-pointer" onClick={() => setIsDesignOpen(!isDesignOpen)}>
                    <h6 className="mb-0 fw-bold text-dark">Customize Design</h6>
                </div>
                <div className={`p-4 \${isDesignOpen ? '' : 'd-none'}`} id="design-section">'''
content = re.sub(old_design, new_design, content)

# Remove the extra </div> from the end of the gray container if any, wait actually, we wrapped it manually in python script 2, 
# wait, in python script 2, we just opened `<div className="p-4 mb-4" style={{ backgroundColor: '#f4f4f5', borderRadius: '24px' }}>`. We need to close it before the right column!

# Let's find where the right column starts:
# `<div className={`col-md-4 ${isBulk ? 'd-none' : ''}`}>`
# We'll replace it to close the gray panel and start the new right column.
old_right_col = r'''</div>
        {/*  Right Column: QR Code Preview  */}
        <div className={`col-md-4 \${isBulk \? 'd-none' : ''}`}>'''
new_right_col = r'''</div>
            </div>
        {/*  Right Column: QR Code Preview  */}
        <div className={`col-md-5 \${isBulk ? 'd-none' : ''}`}>
            <div className="p-4 d-flex flex-column align-items-center" style={{ backgroundColor: '#f4f4f5', borderRadius: '24px' }}>
                <div className="bg-white p-3 shadow-sm mb-4" style={{ borderRadius: '16px', display: 'inline-block' }}>'''
content = re.sub(old_right_col, new_right_col, content)

# Now fix the right column structure.
# Inside right column we have `<div className="card text-center sticky-top" style={{ top: '20px' }}>`
old_qr_card = r'''<div className="card text-center sticky-top" style={{ top: '20px' }}>
                <div className="card-header bg-primary text-white py-3">
                    <h5 className="mb-0"><i className="fas fa-qrcode me-2"></i>Live Preview</h5>
                </div>
                <div className="card-body p-4 d-flex flex-column align-items-center">
                    
                    {/*  The actual QR Code SVG container  */}
                    <div id="qr-code-container" className="mb-4 bg-white p-3 border rounded shadow-sm d-inline-block">'''
new_qr_card = r'''<div className="text-center sticky-top w-100" style={{ top: '20px' }}>
                <div className="d-flex flex-column align-items-center">
                    
                    {/*  The actual QR Code SVG container  */}
                    <div id="qr-code-container" className="mb-4 bg-white p-4 d-inline-block" style={{ borderRadius: '16px' }}>'''
content = re.sub(old_qr_card, new_qr_card, content)


# Now fix the download buttons
old_dl_btns = r'''</div>

                    <div className="d-flex gap-2 w-100 mt-2">
                        <button className="btn btn-outline-primary flex-grow-1" id="download-png" onClick={() => handleSingleDownload(qrRef, 'png', fgColor, bgColor, bodyShape, eyeFrameShape, eyeBallShape, centerLogo, activeTab, getQrData())}><i className="fas fa-image me-1"></i> PNG</button>
                        <button className="btn btn-outline-primary flex-grow-1" id="download-svg" onClick={() => handleSingleDownload(qrRef, 'svg', fgColor, bgColor, bodyShape, eyeFrameShape, eyeBallShape, centerLogo, activeTab, getQrData())}><i className="fas fa-vector-square me-1"></i> SVG</button>
                        <button className="btn btn-outline-primary flex-grow-1" id="download-jpg" onClick={() => handleSingleDownload(qrRef, 'jpeg', fgColor, bgColor, bodyShape, eyeFrameShape, eyeBallShape, centerLogo, activeTab, getQrData())}><i className="fas fa-file-image me-1"></i> JPG</button>
                    </div>
                </div>
            </div>
        </div>
    </div>'''
new_dl_btns = r'''</div>
                    
                    <button className="btn w-100 mb-3 fw-bold text-white shadow-sm" style={{ backgroundColor: '#664ba2', borderRadius: '12px', padding: '12px' }} onClick={(e) => e.preventDefault()}>Generate QR Code</button>

                    <div className="d-flex gap-2 w-100 mt-2">
                        <button className="btn bg-white fw-bold w-50" style={{ borderRadius: '12px', padding: '10px', color: '#333' }} id="download-png" onClick={() => handleSingleDownload(qrRef, 'png', fgColor, bgColor, bodyShape, eyeFrameShape, eyeBallShape, centerLogo, activeTab, getQrData())}>Download PNG</button>
                        <button className="btn bg-white fw-bold w-50" style={{ borderRadius: '12px', padding: '10px', color: '#333' }} id="download-svg" onClick={() => handleSingleDownload(qrRef, 'svg', fgColor, bgColor, bodyShape, eyeFrameShape, eyeBallShape, centerLogo, activeTab, getQrData())}>Download SVG</button>
                    </div>
                </div>
                </div>
            </div>
        </div>
    </div>'''
content = re.sub(old_dl_btns, new_dl_btns, content)

with open('src/app/page.js', 'w') as f:
    f.write(content)
