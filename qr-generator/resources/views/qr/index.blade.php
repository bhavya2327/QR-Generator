@extends('layouts.app')

@section('content')
<div class="container mt-4 mb-5">
    <!-- Top Tabs for Data Types -->
    <div class="d-flex overflow-auto pb-2 mb-4" id="type-tabs" style="gap: 0.5rem; border-bottom: 2px solid var(--border-color);">
        <button class="btn btn-primary type-btn active" data-type="url"><i class="fas fa-link"></i> URL</button>
        <button class="btn btn-outline type-btn" data-type="text"><i class="fas fa-font"></i> Text</button>
        <button class="btn btn-outline type-btn" data-type="email"><i class="fas fa-envelope"></i> Email</button>
        <button class="btn btn-outline type-btn" data-type="phone"><i class="fas fa-phone"></i> Phone</button>
        <button class="btn btn-outline type-btn" data-type="sms"><i class="fas fa-comment"></i> SMS</button>
        <button class="btn btn-outline type-btn" data-type="vcard"><i class="fas fa-id-card"></i> vCard</button>
        <button class="btn btn-outline type-btn" data-type="location"><i class="fas fa-map-marker-alt"></i> Location</button>
        <button class="btn btn-outline type-btn" data-type="wifi"><i class="fas fa-wifi"></i> WiFi</button>
        <button class="btn btn-outline type-btn" data-type="event"><i class="fas fa-calendar-alt"></i> Event</button>
        <button class="btn btn-outline type-btn" data-type="crypto"><i class="fab fa-bitcoin"></i> Crypto</button>
    </div>

    <div class="row">
        <!-- Left Column: Settings -->
        <div class="col-md-8">
            
            <!-- 1. Enter Content -->
            <div class="card mb-3 p-0 overflow-hidden">
                <div class="card-header bg-light d-flex justify-content-between align-items-center p-3" style="border-bottom: 1px solid var(--border-color);">
                    <h5 class="mb-0">1. Enter Content</h5>
                    <div class="form-check form-switch m-0 d-flex align-items-center">
                        <label class="form-check-label me-2 text-muted" for="bulk-toggle-switch" style="font-size: 0.875rem;">Bulk Mode</label>
                        <input class="form-check-input mt-0" type="checkbox" id="bulk-toggle-switch" style="cursor: pointer; width: 2.5em; height: 1.25em;">
                    </div>
                </div>
                <div class="p-4 bg-white" id="content-section">
                    
                    <!-- URL Content Form -->
                    <div id="content-url" class="type-content active">
                        <div id="single-mode-container">
                            <form id="single-qr-form">
                                @csrf
                                <div class="form-group mb-0">
                                    <label for="url" class="text-muted mb-2">Your URL</label>
                                    <input type="url" name="url" id="url" class="form-control" placeholder="https://example.com" required>
                                </div>
                            </form>
                        </div>

                        <div id="bulk-mode-container" style="display: none;">
                            <div id="drop-zone" class="drop-zone py-5">
                                <p class="mb-1 text-primary"><i class="fas fa-cloud-upload-alt fa-2x"></i></p>
                                <p class="mb-2 font-weight-bold">Drag & Drop CSV Here</p>
                                <p class="text-muted small mb-3">or</p>
                                <button class="btn btn-sm btn-outline" id="browse-btn">Browse Files</button>
                                <input type="file" id="csv-file" accept=".csv" style="display: none;">
                            </div>
                            <div class="text-center mt-3">
                                <a href="/sample-csv" class="text-muted" style="font-size: 0.875rem; text-decoration: underline;">Download Sample CSV Format</a>
                            </div>
                            <div id="bulk-error-message" class="text-danger mt-2 text-center" style="display: none;"></div>
                        </div>
                    </div>

                    <!-- Text Content Form -->
                    <div id="content-text" class="type-content" style="display: none;">
                        <div class="form-group mb-0">
                            <label for="text" class="text-muted mb-2">Your Text</label>
                            <textarea id="text" name="text" class="form-control" rows="4" placeholder="Enter your text here..."></textarea>
                        </div>
                    </div>

                    <!-- Email Content Form -->
                    <div id="content-email" class="type-content" style="display: none;">
                        <div class="form-group mb-2">
                            <label for="email" class="text-muted mb-2">Email Address</label>
                            <input type="email" id="email" name="email" class="form-control" placeholder="your@email.com">
                        </div>
                        <div class="form-group mb-2">
                            <label for="email_subject" class="text-muted mb-2">Subject</label>
                            <input type="text" id="email_subject" name="email_subject" class="form-control" placeholder="Subject">
                        </div>
                        <div class="form-group mb-0">
                            <label for="email_body" class="text-muted mb-2">Message</label>
                            <textarea id="email_body" name="email_body" class="form-control" rows="3"></textarea>
                        </div>
                    </div>

                    <!-- Phone Content Form -->
                    <div id="content-phone" class="type-content" style="display: none;">
                        <div class="form-group mb-0">
                            <label for="phone" class="text-muted mb-2">Phone Number</label>
                            <input type="tel" id="phone" name="phone" class="form-control" placeholder="+1234567890">
                        </div>
                    </div>

                    <!-- SMS Content Form -->
                    <div id="content-sms" class="type-content" style="display: none;">
                        <div class="form-group mb-2">
                            <label for="sms_phone" class="text-muted mb-2">Phone Number</label>
                            <input type="tel" id="sms_phone" name="sms_phone" class="form-control" placeholder="+1234567890">
                        </div>
                        <div class="form-group mb-0">
                            <label for="sms_message" class="text-muted mb-2">Message</label>
                            <textarea id="sms_message" name="sms_message" class="form-control" rows="3"></textarea>
                        </div>
                    </div>

                    <!-- vCard Content Form -->
                    <div id="content-vcard" class="type-content" style="display: none;">
                        <div class="row">
                            <div class="col-md-6 form-group mb-2">
                                <label for="vcard_first_name" class="text-muted mb-1">First Name</label>
                                <input type="text" id="vcard_first_name" name="vcard_first_name" class="form-control">
                            </div>
                            <div class="col-md-6 form-group mb-2">
                                <label for="vcard_last_name" class="text-muted mb-1">Last Name</label>
                                <input type="text" id="vcard_last_name" name="vcard_last_name" class="form-control">
                            </div>
                            <div class="col-md-6 form-group mb-2">
                                <label for="vcard_phone" class="text-muted mb-1">Phone</label>
                                <input type="text" id="vcard_phone" name="vcard_phone" class="form-control">
                            </div>
                            <div class="col-md-6 form-group mb-2">
                                <label for="vcard_email" class="text-muted mb-1">Email</label>
                                <input type="email" id="vcard_email" name="vcard_email" class="form-control">
                            </div>
                            <div class="col-md-12 form-group mb-0">
                                <label for="vcard_company" class="text-muted mb-1">Company</label>
                                <input type="text" id="vcard_company" name="vcard_company" class="form-control">
                            </div>
                        </div>
                    </div>

                    <!-- WiFi Content Form -->
                    <div id="content-wifi" class="type-content" style="display: none;">
                        <div class="form-group mb-2">
                            <label for="wifi_ssid" class="text-muted mb-1">Network Name (SSID)</label>
                            <input type="text" id="wifi_ssid" name="wifi_ssid" class="form-control">
                        </div>
                        <div class="form-group mb-2">
                            <label for="wifi_password" class="text-muted mb-1">Password</label>
                            <input type="text" id="wifi_password" name="wifi_password" class="form-control">
                        </div>
                        <div class="form-group mb-0">
                            <label for="wifi_encryption" class="text-muted mb-1">Encryption</label>
                            <select id="wifi_encryption" name="wifi_encryption" class="form-control">
                                <option value="WPA">WPA/WPA2</option>
                                <option value="WEP">WEP</option>
                                <option value="nopass">None</option>
                            </select>
                        </div>
                    </div>
                    
                    <div id="content-location" class="type-content" style="display: none;"><p class="text-muted">Latitude/Longitude fields coming soon...</p></div>
                    <div id="content-event" class="type-content" style="display: none;"><p class="text-muted">Event fields coming soon...</p></div>
                    <div id="content-crypto" class="type-content" style="display: none;"><p class="text-muted">Crypto address fields coming soon...</p></div>
                </div>
            </div>

            <!-- 2. Set Colors -->
            <div class="card mb-3 p-0 overflow-hidden">
                <div class="card-header bg-light p-3 cursor-pointer" style="border-bottom: 1px solid var(--border-color);" onclick="document.getElementById('color-section').classList.toggle('d-none')">
                    <h5 class="mb-0">2. Set Colors</h5>
                </div>
                <div class="p-4 bg-white d-none" id="color-section">
                    <div class="row">
                        <div class="col-md-6 form-group">
                            <label for="color_foreground" class="text-muted mb-2">Foreground Color</label>
                            <input type="color" id="color_foreground" name="color_foreground" class="form-control form-control-color w-100" value="#000000" style="height: 50px;">
                        </div>
                        <div class="col-md-6 form-group">
                            <label for="color_background" class="text-muted mb-2">Background Color</label>
                            <input type="color" id="color_background" name="color_background" class="form-control form-control-color w-100" value="#ffffff" style="height: 50px;">
                        </div>
                    </div>
                </div>
            </div>

            <!-- 3. Add Logo Image -->
            <div class="card mb-3 p-0 overflow-hidden">
                <div class="card-header bg-light p-3 cursor-pointer" style="border-bottom: 1px solid var(--border-color);" onclick="document.getElementById('logo-section').classList.toggle('d-none')">
                    <h5 class="mb-0">3. Add Logo Image</h5>
                </div>
                <div class="p-4 bg-white d-none" id="logo-section">
                    <div class="form-group mb-0">
                        <label for="logo_file" class="text-muted mb-2">Upload Logo (.png)</label>
                        <input type="file" id="logo_file" name="logo_file" class="form-control" accept="image/png">
                        <small class="text-muted mt-1 d-block">A white margin will be added around the logo for readability.</small>
                    </div>
                </div>
            </div>

            <!-- 4. Customize Design -->
            <div class="card mb-3 p-0 overflow-hidden">
                <div class="card-header bg-light p-3 cursor-pointer" style="border-bottom: 1px solid var(--border-color);" onclick="document.getElementById('design-section').classList.toggle('d-none')">
                    <h5 class="mb-0">4. Customize Design</h5>
                </div>
                <div class="p-4 bg-white d-none" id="design-section">
                    <div class="form-group mb-0">
                        <label for="qr_style" class="text-muted mb-2">Body Shape</label>
                        <select id="qr_style" name="qr_style" class="form-control">
                            <option value="square">Square (Default)</option>
                            <option value="dot">Dots</option>
                            <option value="round">Round</option>
                        </select>
                    </div>
                </div>
            </div>

        </div>

        <!-- Right Column: Preview & Action -->
        <div class="col-md-4">
            <div class="card p-3" style="position: sticky; top: 2rem; border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <!-- Live Preview / Loading State -->
                <div id="qr-preview-box" class="qr-preview-box" style="min-height: 250px; display: flex; align-items: center; justify-content: center; background: #f8fafc; border-radius: 0.5rem; margin-bottom: 1rem; border: 1px dashed var(--border-color);">
                    <p class="text-muted m-0" id="preview-placeholder">Your QR Code will appear here</p>
                </div>

                <button class="btn btn-success btn-lg w-100 font-weight-bold" id="main-generate-btn">Create QR Code</button>
                
                <div id="download-actions" style="display: none;" class="mt-3">
                    <div class="d-flex gap-2">
                        <button class="btn btn-primary flex-grow-1" id="download-single-png">Download PNG</button>
                        <button class="btn btn-secondary flex-grow-1" id="download-single-svg">Download SVG</button>
                    </div>
                </div>

                <!-- Bulk Progress / Actions -->
                <div id="bulk-progress-container" style="display: none;" class="mt-4">
                    <p class="mb-2 text-center font-weight-bold">Generating QR Codes...</p>
                    <div class="progress-bar-bg">
                        <div class="progress-bar-fill" id="bulk-progress-fill" style="width: 0%"></div>
                    </div>
                    <p class="text-center mt-2 text-muted" style="font-size: 0.875rem;" id="bulk-progress-text">0% (0 / 0)</p>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Modal for Bulk Preview & Results -->
<div id="bulk-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 1050; align-items: center; justify-content: center;">
    <div class="card p-4" style="width: 90%; max-width: 800px; max-height: 90vh; overflow-y: auto; position: relative;">
        <button id="close-modal-btn" class="btn btn-sm btn-outline text-muted" style="position: absolute; top: 1rem; right: 1rem;">✕ Close</button>
        
        <h3 class="mb-3" id="modal-title">Bulk CSV Preview</h3>
        
        <div id="modal-csv-preview">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <span class="font-weight-bold" id="csv-filename">filename.csv</span>
                <span class="badge" id="csv-stats" style="font-size: 0.9rem;"></span>
            </div>
            
            <div class="table-responsive" style="max-height: 300px;">
                <table class="table table-sm">
                    <thead><tr><th>#</th><th>URL</th><th>Status</th></tr></thead>
                    <tbody id="csv-preview-body"></tbody>
                </table>
            </div>
            <button class="btn btn-success w-100 mt-4" id="modal-start-bulk-btn">Start Generation</button>
        </div>
        
        <div id="modal-bulk-results" style="display: none;">
            <div class="grid-layout mt-3" id="bulk-qr-grid"></div>
            <div class="d-flex gap-2 justify-content-center align-items-center mt-4 border-top pt-4">
                <select id="bulk-download-format" class="form-select" style="max-width: 150px;">
                    <option value="png">PNG</option>
                    <option value="jpg">JPG</option>
                    <option value="svg">SVG</option>
                </select>
                <button class="btn btn-primary" id="download-zip-btn">Download ZIP</button>
            </div>
        </div>
    </div>
</div>
@endsection

