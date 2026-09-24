document.addEventListener('DOMContentLoaded', () => {
    // 1. Data Type Tab Switching
    const typeBtns = document.querySelectorAll('.type-btn');
    const typeContents = document.querySelectorAll('.type-content');
    
    let currentType = 'url'; // default

    typeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active from all
            typeBtns.forEach(b => b.classList.remove('active', 'btn-primary'));
            typeBtns.forEach(b => b.classList.add('btn-outline'));
            
            // Add active to clicked
            btn.classList.remove('btn-outline');
            btn.classList.add('active', 'btn-primary');
            
            // Switch content form
            currentType = btn.dataset.type;
            
            typeContents.forEach(content => {
                if(content.id === `content-${currentType}`) {
                    content.style.display = 'block';
                    content.classList.add('active');
                } else {
                    content.style.display = 'none';
                    content.classList.remove('active');
                }
            });
            
            // Optional: load dynamic fields if not already present
        });
    });

    // 2. Single/Bulk Mode Toggle
    const bulkToggle = document.getElementById('bulk-toggle-switch');
    const singleContainer = document.getElementById('single-mode-container');
    const bulkContainer = document.getElementById('bulk-mode-container');
    
    let isBulkMode = false;

    if (bulkToggle) {
        bulkToggle.addEventListener('change', (e) => {
            isBulkMode = e.target.checked;
            if (isBulkMode) {
                singleContainer.style.display = 'none';
                bulkContainer.style.display = 'block';
            } else {
                singleContainer.style.display = 'block';
                bulkContainer.style.display = 'none';
            }
        });
    }

    // 3. Single Generate Logic
    const mainGenerateBtn = document.getElementById('main-generate-btn');
    const previewBox = document.getElementById('qr-preview-box');
    const previewPlaceholder = document.getElementById('preview-placeholder');
    const downloadActions = document.getElementById('download-actions');
    const downloadPng = document.getElementById('download-single-png');
    const downloadSvg = document.getElementById('download-single-svg');
    
    mainGenerateBtn.addEventListener('click', async () => {
        if (isBulkMode) {
            // In bulk mode, generation is handled after CSV preview in the modal
            alert("Please upload a CSV file to generate bulk QR codes.");
            return;
        }

        // Gather single form data based on currentType
        const token = document.querySelector('input[name="_token"]')?.value;
        const formData = new FormData();
        formData.append('_token', token);
        formData.append('type', currentType);
        
        // 1. Enter Content fields
        if (currentType === 'url') {
            const urlInput = document.getElementById('url').value;
            if(!urlInput) { alert('Please enter a URL'); return; }
            formData.append('url', urlInput);
        } else if (currentType === 'text') {
            const textInput = document.getElementById('text').value;
            if(!textInput) { alert('Please enter some text'); return; }
            formData.append('text', textInput);
        } else if (currentType === 'email') {
            formData.append('email', document.getElementById('email').value);
            formData.append('email_subject', document.getElementById('email_subject').value);
            formData.append('email_body', document.getElementById('email_body').value);
        } else if (currentType === 'phone') {
            formData.append('phone', document.getElementById('phone').value);
        } else if (currentType === 'sms') {
            formData.append('sms_phone', document.getElementById('sms_phone').value);
            formData.append('sms_message', document.getElementById('sms_message').value);
        } else if (currentType === 'vcard') {
            formData.append('vcard_first_name', document.getElementById('vcard_first_name').value);
            formData.append('vcard_last_name', document.getElementById('vcard_last_name').value);
            formData.append('vcard_phone', document.getElementById('vcard_phone').value);
            formData.append('vcard_email', document.getElementById('vcard_email').value);
            formData.append('vcard_company', document.getElementById('vcard_company').value);
        } else if (currentType === 'wifi') {
            formData.append('wifi_ssid', document.getElementById('wifi_ssid').value);
            formData.append('wifi_password', document.getElementById('wifi_password').value);
            formData.append('wifi_encryption', document.getElementById('wifi_encryption').value);
        }

        // Customizations
        formData.append('color_foreground', document.getElementById('color_foreground').value);
        formData.append('color_background', document.getElementById('color_background').value);
        formData.append('qr_style', document.getElementById('qr_style').value);

        const logoFile = document.getElementById('logo_file').files[0];
        if (logoFile) {
            formData.append('logo_file', logoFile);
        }

        // Show loading state
        const originalText = mainGenerateBtn.innerHTML;
        mainGenerateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        mainGenerateBtn.disabled = true;

        try {
            const response = await fetch('/qr/generate', {
                method: 'POST',
                body: formData,
                headers: { 'Accept': 'application/json' }
            });
            const result = await response.json();
            
            if (response.ok && result.success) {
                previewPlaceholder.style.display = 'none';
                
                // Remove old SVG if exists
                const oldSvg = previewBox.querySelector('svg');
                if (oldSvg) oldSvg.remove();
                
                // Inject new SVG
                previewBox.insertAdjacentHTML('beforeend', result.svg);
                
                // Set downloads
                downloadPng.onclick = () => window.location.href = `/qr/${result.id}/png`;
                downloadSvg.onclick = () => window.location.href = `/qr/${result.id}/svg`;
                
                downloadActions.style.display = 'block';
            } else {
                alert(result.message || 'Error generating QR code');
            }
        } catch (err) {
            alert('A network error occurred.');
        } finally {
            mainGenerateBtn.innerHTML = originalText;
            mainGenerateBtn.disabled = false;
        }
    });

    // 4. Bulk Drag and Drop & CSV Logic
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('csv-file');
    const browseBtn = document.getElementById('browse-btn');
    const bulkErrorMsg = document.getElementById('bulk-error-message');
    const bulkModal = document.getElementById('bulk-modal');
    
    if (dropZone && fileInput) {
        browseBtn.addEventListener('click', (e) => { e.preventDefault(); fileInput.click(); });

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                handleFileUpload(fileInput.files[0]);
            }
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) {
                handleFileUpload(fileInput.files[0]);
            }
        });
    }

    async function handleFileUpload(file) {
        bulkErrorMsg.style.display = 'none';
        
        if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
            bulkErrorMsg.textContent = 'Please upload a valid .csv file.';
            bulkErrorMsg.style.display = 'block';
            return;
        }

        const formData = new FormData();
        formData.append('csv_file', file);
        const token = document.querySelector('input[name="_token"]');
        if(token) formData.append('_token', token.value);

        try {
            const response = await fetch('/csv/upload', {
                method: 'POST',
                body: formData,
                headers: { 'Accept': 'application/json' }
            });
            const result = await response.json();

            if (response.ok && result.success) {
                showBulkModal(result.filename, result.data);
            } else {
                bulkErrorMsg.textContent = result.message || 'Error processing file.';
                bulkErrorMsg.style.display = 'block';
            }
        } catch (error) {
            bulkErrorMsg.textContent = 'An error occurred during upload.';
            bulkErrorMsg.style.display = 'block';
        }
    }

    // 5. Bulk Modal Logic
    let currentBulkRecords = [];
    
    document.getElementById('close-modal-btn').addEventListener('click', () => {
        bulkModal.style.display = 'none';
    });

    function showBulkModal(filename, data) {
        currentBulkRecords = data.records;
        
        document.getElementById('csv-filename').textContent = filename;
        document.getElementById('csv-stats').textContent = `Total: ${data.total} | Valid: ${data.valid} | Invalid: ${data.invalid}`;
        
        const previewBody = document.getElementById('csv-preview-body');
        previewBody.innerHTML = '';
        
        data.records.forEach(record => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${record.index}</td>
                <td class="text-truncate" style="max-width: 250px;">${record.url}</td>
                <td class="status-${record.status}">${record.status}</td>
            `;
            previewBody.appendChild(tr);
        });

        document.getElementById('modal-csv-preview').style.display = 'block';
        document.getElementById('modal-bulk-results').style.display = 'none';
        bulkModal.style.display = 'flex';
    }

    document.getElementById('modal-start-bulk-btn').addEventListener('click', async () => {
        const validUrls = currentBulkRecords.filter(r => r.status === 'Valid').map(r => r.url);
        if (validUrls.length === 0) return alert('No valid records to generate.');

        document.getElementById('modal-csv-preview').style.display = 'none';
        document.getElementById('modal-bulk-results').style.display = 'block';
        
        const gridContainer = document.getElementById('bulk-qr-grid');
        gridContainer.innerHTML = '';
        
        // Use the main view's progress bar (move it to modal logic ideally, or show simple loading)
        // For brevity in UI refactor, let's just make the bulk calls.
        
        const token = document.querySelector('input[name="_token"]')?.value || '';
        const chunkSize = 10;
        
        for (let i = 0; i < validUrls.length; i += chunkSize) {
            const chunk = validUrls.slice(i, i + chunkSize);
            
            // Gather custom options for bulk
            const options = {
                color_foreground: document.getElementById('color_foreground').value,
                color_background: document.getElementById('color_background').value,
                qr_style: document.getElementById('qr_style').value
            };

            // Cannot easily send File in JSON, skip logo for bulk for now unless we use FormData
            
            try {
                const response = await fetch('/qr/bulk-generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'X-CSRF-TOKEN': token
                    },
                    body: JSON.stringify({ urls: chunk, options: options })
                });
                const result = await response.json();
                if (response.ok && result.success) {
                    gridContainer.innerHTML = `
                        <div class="text-center py-5">
                            <i class="fas fa-check-circle text-success" style="font-size: 4rem;"></i>
                            <h4 class="mt-3">QR Codes Generated Successfully!</h4>
                            <p class="text-muted">Your ${validUrls.length} QR codes are ready for download.</p>
                        </div>
                    `;
                }
            } catch (e) {
                console.error(e);
            }
        }
        
        // Bind ZIP download in modal
        document.getElementById('download-zip-btn').onclick = () => {
            const format = document.getElementById('bulk-download-format').value;
            downloadZip(validUrls, format);
        };
    });

    async function downloadZip(urls, format) {
        const token = document.querySelector('input[name="_token"]')?.value || '';
        const btnId = 'download-zip-btn';
        const btn = document.getElementById(btnId);
        const originalText = btn.textContent;
        btn.textContent = 'Generating ZIP...';
        btn.disabled = true;

        try {
            const response = await fetch('/qr/download-zip', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRF-TOKEN': token },
                body: JSON.stringify({ urls, format, options: {
                    color_foreground: document.getElementById('color_foreground').value,
                    color_background: document.getElementById('color_background').value,
                    qr_style: document.getElementById('qr_style').value
                } })
            });

            if (!response.ok) {
                // Check if it's the imagick error to give a better message
                if (response.status === 500) {
                    throw new Error('Server Error: PNG generation requires the "imagick" PHP extension installed on your system. Please use SVG for now or enable imagick.');
                }
                throw new Error('Failed to generate ZIP');
            }
            
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = downloadUrl;
            a.download = `qr-codes-${format}.zip`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(downloadUrl);
            a.remove();
            
            // Show responsive success popup
            alert(`✅ Success! Your ${format.toUpperCase()} ZIP file has been downloaded.`);

        } catch (err) {
            alert('❌ ' + err.message);
        } finally {
            btn.textContent = originalText;
            btn.disabled = false;
        }
    }
});
