'use client';
import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import QRCodePreview from '../components/QRCodePreview';
import { handleSingleDownload } from '../utils/qrUtils';
import Papa from 'papaparse';
import QRCodeStyling from 'qr-code-styling';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';

export default function Page() {
    
    // Tab State
    const [activeTab, setActiveTab] = useState('url');
    const [isBulk, setIsBulk] = useState(false);
    
    // Core Generation States
    const [fgColor, setFgColor] = useState('#000000');
    const [bgColor, setBgColor] = useState('#ffffff');
    const [bodyShape, setBodyShape] = useState('square');
    const [isContentOpen, setIsContentOpen] = useState(true);
    const [isColorOpen, setIsColorOpen] = useState(false);
    const [isLogoOpen, setIsLogoOpen] = useState(false);
    const [isDesignOpen, setIsDesignOpen] = useState(false);

    const [eyeFrameShape, setEyeFrameShape] = useState('square');
    const [eyeBallShape, setEyeBallShape] = useState('square');
    const [centerLogo, setCenterLogo] = useState(null);

    // Data States
    const [url, setUrl] = useState('https://example.com');
    const [text, setText] = useState('');
    const [email, setEmail] = useState('');
    const [emailSub, setEmailSub] = useState('');
    const [emailBody, setEmailBody] = useState('');
    const [phone, setPhone] = useState('');
    const [smsNumber, setSmsNumber] = useState('');
    const [smsMessage, setSmsMessage] = useState('');
    
    // vCard
    const [vcardFirst, setVcardFirst] = useState('');
    const [vcardLast, setVcardLast] = useState('');
    const [vcardMobile, setVcardMobile] = useState('');
    const [vcardPhone, setVcardPhone] = useState('');
    const [vcardFax, setVcardFax] = useState('');
    const [vcardEmail, setVcardEmail] = useState('');
    const [vcardCompany, setVcardCompany] = useState('');
    const [vcardDesc, setVcardDesc] = useState('');
    const [vcardJob, setVcardJob] = useState('');
    const [vcardStreet, setVcardStreet] = useState('');
    const [vcardCity, setVcardCity] = useState('');
    const [vcardZip, setVcardZip] = useState('');
    const [vcardState, setVcardState] = useState('');
    const [vcardCountry, setVcardCountry] = useState('');
    const [vcardWebsite, setVcardWebsite] = useState('');
    const [vcardLinkedIn, setVcardLinkedIn] = useState('');
    const [vcardInstagram, setVcardInstagram] = useState('');
    const [vcardFacebook, setVcardFacebook] = useState('');
    const [vcardYoutube, setVcardYoutube] = useState('');
    const [scPhotoUrl, setScPhotoUrl] = useState('');
    
    // Location
    const [locStreet, setLocStreet] = useState('');
    const [locCity, setLocCity] = useState('');
    const [locState, setLocState] = useState('');
    const [locZip, setLocZip] = useState('');

    // Event
    const [eventName, setEventName] = useState('');
    const [eventLoc, setEventLoc] = useState('');
    const [eventStart, setEventStart] = useState('');
    const [eventEnd, setEventEnd] = useState('');

    // Convert Google Drive / Dropbox sharing links to direct download URLs and wrap in CORS proxy
    const toDirectPhotoUrl = (url) => {
        if (!url) return '';
        if (url.startsWith('data:')) return url;
        
        let directUrl = url;
        const driveMatch = url.match(/drive\.google\.com\/file\/d\/([^/]+)/);
        if (driveMatch) directUrl = `https://lh3.googleusercontent.com/d/${driveMatch[1]}`;
        const driveMatch2 = url.match(/drive\.google\.com\/open\?id=([^&]+)/);
        if (driveMatch2) directUrl = `https://lh3.googleusercontent.com/d/${driveMatch2[1]}`;
        if (url.includes('dropbox.com')) directUrl = url.replace('dl=0', 'dl=1');
        
        return `https://corsproxy.io/?${encodeURIComponent(directUrl)}`;
    };

    const handleCenterLogoUpload = (e) => {
        const file = e.target.files[0];
        if (!file) {
            setCenterLogo(null);
            return;
        }
        const reader = new FileReader();
        reader.onload = (ev) => {
            setCenterLogo(ev.target.result);
        };
        reader.readAsDataURL(file);
    };



    const getQrData = () => {
        if (activeTab === 'url') return url || 'https://example.com';
        if (activeTab === 'text') return text || 'Text';
        if (activeTab === 'email') return `MATMSG:TO:${email};SUB:${emailSub};BODY:${emailBody};;`;
        if (activeTab === 'phone') return `tel:${phone}`;
        if (activeTab === 'sms') return `smsto:${smsNumber}:${smsMessage}`;
        if (activeTab === 'vcard') {
            return `BEGIN:VCARD
VERSION:3.0
N:${vcardLast};${vcardFirst}
FN:${vcardFirst} ${vcardLast}
ORG:${vcardCompany}
TITLE:${vcardJob}
NOTE:${vcardDesc}
TEL;TYPE=work,voice:${vcardPhone}
TEL;TYPE=cell,voice:${vcardMobile}
TEL;TYPE=fax:${vcardFax}
EMAIL:${vcardEmail}
${vcardWebsite ? `URL:${vcardWebsite}\n` : ''}${vcardLinkedIn ? `X-SOCIALPROFILE;type=linkedin:${vcardLinkedIn}\n` : ''}${vcardInstagram ? `X-SOCIALPROFILE;type=instagram:${vcardInstagram}\n` : ''}${vcardFacebook ? `X-SOCIALPROFILE;type=facebook:${vcardFacebook}\n` : ''}${vcardYoutube ? `X-SOCIALPROFILE;type=youtube:${vcardYoutube}\n` : ''}ADR;TYPE=work:;;${vcardStreet};${vcardCity};${vcardState};${vcardZip};${vcardCountry}
END:VCARD`;
        }
        if (activeTab === 'smartcard') {
            const data = {
                firstName: vcardFirst, lastName: vcardLast, phone: vcardPhone, email: vcardEmail,
                company: vcardCompany, job: vcardJob, desc: vcardDesc,
                website: vcardWebsite, linkedin: vcardLinkedIn, facebook: vcardFacebook,
                instagram: vcardInstagram, youtube: vcardYoutube, photo: scPhotoUrl
            };
            const payload = btoa(encodeURIComponent(JSON.stringify(data)));
            return `${window.location.origin}/QR-Generator/card?data=${payload}`;
        }
        if (activeTab === 'location') {
            const query = encodeURIComponent(`${locStreet} ${locCity} ${locState} ${locZip}`.trim());
            return query ? `https://www.google.com/maps/search/?api=1&query=${query}` : 'https://www.google.com/maps';
        }
        if (activeTab === 'event') {
            const formatDT = (dt) => dt ? dt.replace(/[-:]/g, '') + 'Z' : '';
            return `BEGIN:VEVENT\nSUMMARY:${eventName}\nLOCATION:${eventLoc}\nDTSTART:${formatDT(eventStart)}\nDTEND:${formatDT(eventEnd)}\nEND:VEVENT`;
        }
        return 'https://example.com';
    };


    
    const [isBulkProcessing, setIsBulkProcessing] = useState(false);
    const [bulkProgress, setBulkProgress] = useState(0);
    const [bulkText, setBulkText] = useState('');
    
    // New states for the Bulk Preview Modal
    const [showBulkModal, setShowBulkModal] = useState(false);
    const [bulkRecords, setBulkRecords] = useState([]);
    const [bulkFilename, setBulkFilename] = useState('');
    const [bulkStage, setBulkStage] = useState('preview'); // 'preview' | 'generating' | 'done'
    const [bulkFormat, setBulkFormat] = useState('png');

    // Define expected columns and validation per tab
    const bulkColumnConfig = {
        url: { columns: ['url', 'logo_url'], label: 'URL', validate: (row) => row.url && row.url.startsWith('http') },
        text: { columns: ['text', 'logo_url'], label: 'Text', validate: (row) => row.text && row.text.trim().length > 0 },
        email: { columns: ['email', 'subject', 'body', 'logo_url'], label: 'Email', validate: (row) => row.email && row.email.includes('@') },
        phone: { columns: ['phone', 'logo_url'], label: 'Phone', validate: (row) => row.phone && row.phone.trim().length > 0 },
        sms: { columns: ['phone', 'message', 'logo_url'], label: 'SMS', validate: (row) => row.phone && row.phone.trim().length > 0 },
        vcard: { columns: ['first_name', 'last_name', 'phone', 'email', 'company', 'description', 'website', 'linkedin', 'facebook', 'instagram', 'youtube', 'logo_url'], label: 'vCard', validate: (row) => row.first_name && row.first_name.trim().length > 0 },
        smartcard: { columns: ['first_name', 'last_name', 'phone', 'email', 'company', 'description', 'website', 'linkedin', 'facebook', 'instagram', 'youtube', 'photo_url', 'logo_url'], label: 'SmartCard', validate: (row) => row.first_name && row.first_name.trim().length > 0 },
        location: { columns: ['street', 'city', 'state', 'zip', 'logo_url'], label: 'Location', validate: (row) => (row.street || row.city) && (row.street + row.city).trim().length > 0 },
        event: { columns: ['name', 'location', 'start', 'end', 'logo_url'], label: 'Event', validate: (row) => row.name && row.name.trim().length > 0 },
    };

    // Convert a parsed CSV row into QR-encodable data based on the active tab
    const rowToQrData = (row, tab) => {
        if (tab === 'url') return row.url;
        if (tab === 'text') return row.text;
        if (tab === 'email') return `MATMSG:TO:${row.email || ''};SUB:${row.subject || ''};BODY:${row.body || ''};;`;
        if (tab === 'phone') return `tel:${row.phone}`;
        if (tab === 'sms') return `smsto:${row.phone || ''}:${row.message || ''}`;
        if (tab === 'vcard') {
            const getSocial = (type, val) => val ? `X-SOCIALPROFILE;type=${type}:${val}\n` : '';
            const website = row.website ? `URL:${row.website}\n` : '';
            return `BEGIN:VCARD\nVERSION:3.0\nN:${row.last_name || ''};${row.first_name || ''}\nFN:${row.first_name || ''} ${row.last_name || ''}\nORG:${row.company || ''}\nNOTE:${row.description || ''}\nTEL:${row.phone || ''}\nEMAIL:${row.email || ''}\n${website}${getSocial('linkedin', row.linkedin)}${getSocial('instagram', row.instagram)}${getSocial('facebook', row.facebook)}${getSocial('youtube', row.youtube)}END:VCARD`;
        }
        if (tab === 'smartcard') {
            const data = {
                firstName: row.first_name, lastName: row.last_name, phone: row.phone, email: row.email,
                company: row.company, desc: row.description, website: row.website,
                linkedin: row.linkedin, facebook: row.facebook, instagram: row.instagram, 
                youtube: row.youtube, photo: row.photo_url ? toDirectPhotoUrl(row.photo_url) : ''
            };
            const payload = btoa(encodeURIComponent(JSON.stringify(data)));
            return `${window.location.origin}/QR-Generator/card?data=${payload}`;
        }
        if (tab === 'location') {
            const query = encodeURIComponent(`${row.street || ''} ${row.city || ''} ${row.state || ''} ${row.zip || ''}`.trim());
            return `https://www.google.com/maps/search/?api=1&query=${query}`;
        }
        if (tab === 'event') {
            const formatDT = (dt) => dt ? dt.replace(/[-:T]/g, '') + 'Z' : '';
            return `BEGIN:VEVENT\nSUMMARY:${row.name || ''}\nLOCATION:${row.location || ''}\nDTSTART:${formatDT(row.start)}\nDTEND:${formatDT(row.end)}\nEND:VEVENT`;
        }
        return '';
    };

    const onFileUpload = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        setBulkFilename(file.name);
        const config = bulkColumnConfig[activeTab];
        
        Papa.parse(file, {
            header: true,
            skipEmptyLines: true,
            // Convert header to lowercase and trim spaces to be more forgiving
            transformHeader: (header) => header.trim().toLowerCase(),
            complete: (results) => {
                const records = results.data.map((row, idx) => {
                    // Build a display summary from the first column value
                    const firstCol = config.columns[0];
                    const displayVal = row[firstCol] || '(empty)';
                    return {
                        index: idx + 1,
                        data: row,
                        display: displayVal,
                        status: config.validate(row) ? 'Valid' : 'Invalid'
                    };
                });
                setBulkRecords(records);
                setBulkStage('preview');
                setShowBulkModal(true);
            }
        });
    };

    const startBulkGeneration = async () => {
        const validRecords = bulkRecords.filter(r => r.status === 'Valid');
        if (validRecords.length === 0) return alert('No valid records found.');
        
        setBulkStage('generating');
        
        try {
            const zip = new JSZip();
            const total = validRecords.length;

            for (let i = 0; i < total; i++) {
                const rowData = validRecords[i].data;
                const qrData = rowToQrData(rowData, activeTab);
                const rowLogoUrl = rowData.logo_url ? toDirectPhotoUrl(rowData.logo_url) : centerLogo;

                const qrCode = new QRCodeStyling({
                    width: 300, height: 300, type: "svg", data: qrData,
                    image: rowLogoUrl,
                    qrOptions: { errorCorrectionLevel: 'H' },
                    dotsOptions: { color: fgColor, type: bodyShape },
                    cornersSquareOptions: { color: fgColor, type: eyeFrameShape },
                    cornersDotOptions: { color: fgColor, type: eyeBallShape },
                    backgroundOptions: { color: bgColor },
                    imageOptions: { crossOrigin: "anonymous", margin: 5, imageSize: 0.4 }
                });

                const blob = await qrCode.getRawData(bulkFormat);
                if (blob) zip.file(`qr-${i + 1}.${bulkFormat}`, blob);
                
                setBulkProgress(Math.round(((i + 1) / total) * 100));
                setBulkText(`${Math.round(((i + 1) / total) * 100)}% (${i + 1} / ${total})`);
            }

            const content = await zip.generateAsync({ type: "blob" });
            saveAs(content, `bulk-qrs-${bulkFormat}.zip`);
            
            setBulkStage('done');
        } catch(e) {
            console.error(e);
            alert('Failed to process bulk CSV.');
            setShowBulkModal(false);
        }
    };

    return (
        <div className="container mt-4 mb-5">
            


<div className="container mt-4 mb-5">
    {/*  Top Tabs for Data Types  */}
    <div className="d-flex overflow-auto pb-2 mb-4" id="type-tabs" >
        <button className={`btn type-btn ${activeTab === "url" ? "btn-primary active" : "btn-outline"}`} onClick={() => setActiveTab("url")}><i className="fas fa-link"></i> URL</button>
        <button className={`btn type-btn ${activeTab === "text" ? "btn-primary active" : "btn-outline"}`} onClick={() => setActiveTab("text")}><i className="fas fa-font"></i> Text</button>
        <button className={`btn type-btn ${activeTab === "email" ? "btn-primary active" : "btn-outline"}`} onClick={() => setActiveTab("email")}><i className="fas fa-envelope"></i> Email</button>
        <button className={`btn type-btn ${activeTab === "phone" ? "btn-primary active" : "btn-outline"}`} onClick={() => setActiveTab("phone")}><i className="fas fa-phone"></i> Phone</button>
        <button className={`btn type-btn ${activeTab === "sms" ? "btn-primary active" : "btn-outline"}`} onClick={() => setActiveTab("sms")}><i className="fas fa-comment"></i> SMS</button>
        <button className={`btn type-btn ${activeTab === "vcard" ? "btn-primary active" : "btn-outline"}`} onClick={() => setActiveTab("vcard")}><i className="fas fa-id-card"></i> vCard</button>
        <button className={`btn type-btn ${activeTab === "smartcard" ? "btn-primary active" : "btn-outline"}`} onClick={() => setActiveTab("smartcard")}><i className="fas fa-id-badge"></i> Smart Card</button>
        <button className={`btn type-btn ${activeTab === "location" ? "btn-primary active" : "btn-outline"}`} onClick={() => setActiveTab("location")}><i className="fas fa-map-marker-alt"></i> Location</button>
                <button className={`btn type-btn ${activeTab === "event" ? "btn-primary active" : "btn-outline"}`} onClick={() => setActiveTab("event")}><i className="fas fa-calendar-alt"></i> Event</button>
            </div>

    <div className="row">
        {/*  Left Column: Settings  */}
        <div className={`col-md-${isBulk ? 12 : 8}`}>
            
            {/*  1. Enter Content  */}
            <div className="card mb-3 p-0 overflow-hidden">
                <div className="card-header bg-transparent-glass-header d-flex justify-content-between align-items-center p-3 cursor-pointer" style={{ borderBottom: '1px solid var(--border-color)', cursor: 'pointer' }} onClick={() => setIsContentOpen(!isContentOpen)}>
                    <h5 className="mb-0">1. Enter Content</h5>
                    <div className="d-flex align-items-center gap-3">
                        <div className="form-check form-switch m-0 d-flex align-items-center" onClick={(e) => e.stopPropagation()}>
                            <label className="form-check-label me-2 text-muted" htmlFor="bulk-toggle-switch" style={{ fontSize: '0.875rem' }}>Bulk Mode</label>
                            <input className="form-check-input mt-0" type="checkbox" id="bulk-toggle-switch" style={{ cursor: 'pointer', width: '2.5em', height: '1.25em', marginLeft: '0.5rem' }} checked={isBulk} onChange={(e) => setIsBulk(e.target.checked)} />
                        </div>
                        <i className={`fas ${isContentOpen ? 'fa-chevron-up' : 'fa-chevron-down'} text-muted`}></i>
                    </div>
                </div>
                <div className={`p-4 bg-transparent-glass ${isContentOpen ? '' : 'd-none'}`} id="content-section">
                    <div className={isBulk ? "d-none" : ""}>
                    
                    {/*  URL Content Form  */}
                    <div id="content-url" className={`type-content ${activeTab === 'url' ? 'active' : 'd-none'}`}>
                        
                            <form id="single-qr-form">
                                
                                <div className="form-group mb-0">
                                    <label htmlFor="url" className="text-muted mb-2">Your URL</label>
                                    <input type="url" name="url" id="url" className="form-control" placeholder="https://example.com" required value={url} onChange={(e) => setUrl(e.target.value)} />
                                </div>
                            </form>
                    </div>

                    {/*  Text Content Form  */}
                    <div id="content-text" className={`type-content ${activeTab === "text" ? "" : "d-none"}`} >
                        <div className="form-group mb-0">
                            <label htmlFor="text" className="text-muted mb-2">Your Text</label>
                            <textarea id="text" name="text" className="form-control" rows="4" placeholder="Enter your text here..." value={text} onChange={(e) => setText(e.target.value)}></textarea>
                        </div>
                    </div>

                    {/*  Email Content Form  */}
                    <div id="content-email" className={`type-content ${activeTab === "email" ? "" : "d-none"}`} >
                        <div className="form-group mb-2">
                            <label htmlFor="email" className="text-muted mb-2">Email Address</label>
                            <input type="email" id="email" name="email" className="form-control" placeholder="your@email.com" value={email} onChange={(e) => setEmail(e.target.value)} />
                        </div>
                        <div className="form-group mb-2">
                            <label htmlFor="email_subject" className="text-muted mb-2">Subject</label>
                            <input type="text" id="email_subject" name="email_subject" className="form-control" placeholder="Subject" value={emailSub} onChange={(e) => setEmailSub(e.target.value)} />
                        </div>
                        <div className="form-group mb-0">
                            <label htmlFor="email_body" className="text-muted mb-2">Message</label>
                            <textarea id="email_body" name="email_body" className="form-control" rows="3" value={emailBody} onChange={(e) => setEmailBody(e.target.value)}></textarea>
                        </div>
                    </div>

                    {/*  Phone Content Form  */}
                    <div id="content-phone" className={`type-content ${activeTab === "phone" ? "" : "d-none"}`} >
                        <div className="form-group mb-0">
                            <label htmlFor="phone" className="text-muted mb-2">Phone Number</label>
                            <input type="tel" id="phone" name="phone" className="form-control" placeholder="+1234567890" value={phone} onChange={(e) => setPhone(e.target.value)} />
                        </div>
                    </div>

                    {/*  SMS Content Form  */}
                    <div id="content-sms" className={`type-content ${activeTab === "sms" ? "" : "d-none"}`} >
                        <div className="form-group mb-2">
                            <label htmlFor="sms_phone" className="text-muted mb-2">Phone Number</label>
                            <input type="tel" id="sms_phone" name="sms_phone" className="form-control" placeholder="+1234567890" value={smsNumber} onChange={(e) => setSmsNumber(e.target.value)} />
                        </div>
                        <div className="form-group mb-0">
                            <label htmlFor="sms_message" className="text-muted mb-2">Message</label>
                            <textarea id="sms_message" name="sms_message" className="form-control" rows="3" value={smsMessage} onChange={(e) => setSmsMessage(e.target.value)}></textarea>
                        </div>
                    </div>

                    {/*  vCard / SmartCard Content Form  */}
                    <div id="content-vcard" className={`type-content ${activeTab === "vcard" || activeTab === "smartcard" ? "" : "d-none"}`} >
                        <div className="row">
                            <div className="col-md-6 form-group mb-2">
                                <label htmlFor="vcard_first_name" className="text-muted mb-1">First Name</label>
                                <input type="text" id="vcard_first_name" name="vcard_first_name" className="form-control" value={vcardFirst} onChange={(e) => setVcardFirst(e.target.value)} />
                            </div>
                            <div className="col-md-6 form-group mb-2">
                                <label htmlFor="vcard_last_name" className="text-muted mb-1">Last Name</label>
                                <input type="text" id="vcard_last_name" name="vcard_last_name" className="form-control" value={vcardLast} onChange={(e) => setVcardLast(e.target.value)} />
                            </div>
                            <div className="col-md-6 form-group mb-2">
                                <label htmlFor="vcard_phone" className="text-muted mb-1">Phone</label>
                                <input type="text" id="vcard_phone" name="vcard_phone" className="form-control" value={vcardPhone} onChange={(e) => setVcardPhone(e.target.value)} />
                            </div>
                            <div className="col-md-6 form-group mb-2">
                                <label htmlFor="vcard_email" className="text-muted mb-1">Email</label>
                                <input type="email" id="vcard_email" name="vcard_email" className="form-control" value={vcardEmail} onChange={(e) => setVcardEmail(e.target.value)} />
                            </div>
                            <div className="col-md-12 form-group mb-2">
                                <label htmlFor="vcard_company" className="text-muted mb-1">Company</label>
                                <input type="text" id="vcard_company" name="vcard_company" className="form-control" value={vcardCompany} onChange={(e) => setVcardCompany(e.target.value)} />
                            </div>
                            <div className="col-md-12 form-group mb-0">
                                <label htmlFor="vcard_desc" className="text-muted mb-1">Description</label>
                                <textarea id="vcard_desc" name="vcard_desc" className="form-control" rows="3" value={vcardDesc} onChange={(e) => setVcardDesc(e.target.value)}></textarea>
                            </div>
                            
                            {activeTab === 'smartcard' && (
                                <div className="col-md-12 form-group mt-3 mb-2">
                                    <label htmlFor="sc_photo_url" className="text-muted mb-1">Profile Photo URL (Required for Smart Card)</label>
                                    <input type="url" id="sc_photo_url" className="form-control" placeholder="https://" value={scPhotoUrl} onChange={(e) => setScPhotoUrl(e.target.value)} />
                                    <small className="text-muted mt-1 d-block">Paste a link to your profile picture (Imgur, Drive, etc.).</small>
                                </div>
                            )}

                            <div className="col-md-12 mt-4 mb-2">
                                <h6>Social Media & Links</h6>
                                <hr className="mt-1 mb-3" />
                            </div>
                            <div className="col-md-6 form-group mb-2">
                                <label htmlFor="vcard_website" className="text-muted mb-1">Company / Website URL</label>
                                <input type="url" id="vcard_website" className="form-control" placeholder="https://" value={vcardWebsite} onChange={(e) => setVcardWebsite(e.target.value)} />
                            </div>
                            <div className="col-md-6 form-group mb-2">
                                <label htmlFor="vcard_linkedin" className="text-muted mb-1">LinkedIn URL</label>
                                <input type="url" id="vcard_linkedin" className="form-control" placeholder="https://" value={vcardLinkedIn} onChange={(e) => setVcardLinkedIn(e.target.value)} />
                            </div>
                            <div className="col-md-6 form-group mb-2">
                                <label htmlFor="vcard_facebook" className="text-muted mb-1">Facebook URL</label>
                                <input type="url" id="vcard_facebook" className="form-control" placeholder="https://" value={vcardFacebook} onChange={(e) => setVcardFacebook(e.target.value)} />
                            </div>
                            <div className="col-md-6 form-group mb-2">
                                <label htmlFor="vcard_instagram" className="text-muted mb-1">Instagram URL</label>
                                <input type="url" id="vcard_instagram" className="form-control" placeholder="https://" value={vcardInstagram} onChange={(e) => setVcardInstagram(e.target.value)} />
                            </div>
                            <div className="col-md-6 form-group mb-2">
                                <label htmlFor="vcard_youtube" className="text-muted mb-1">YouTube URL</label>
                                <input type="url" id="vcard_youtube" className="form-control" placeholder="https://" value={vcardYoutube} onChange={(e) => setVcardYoutube(e.target.value)} />
                            </div>
                        </div>
                    </div>

                    {/*  Location Content Form  */}
                    <div id="content-location" className={`type-content ${activeTab === "location" ? "" : "d-none"}`}>
                        <div className="form-group mb-2">
                            <label htmlFor="loc_street" className="text-muted mb-1">Street Address</label>
                            <input type="text" id="loc_street" className="form-control" placeholder="123 Main St" value={locStreet} onChange={(e) => setLocStreet(e.target.value)} />
                        </div>
                        <div className="row">
                            <div className="col-md-4 form-group mb-2">
                                <label htmlFor="loc_city" className="text-muted mb-1">City</label>
                                <input type="text" id="loc_city" className="form-control" placeholder="New York" value={locCity} onChange={(e) => setLocCity(e.target.value)} />
                            </div>
                            <div className="col-md-4 form-group mb-2">
                                <label htmlFor="loc_state" className="text-muted mb-1">State</label>
                                <input type="text" id="loc_state" className="form-control" placeholder="NY" value={locState} onChange={(e) => setLocState(e.target.value)} />
                            </div>
                            <div className="col-md-4 form-group mb-2">
                                <label htmlFor="loc_zip" className="text-muted mb-1">Pin/Zip Code</label>
                                <input type="text" id="loc_zip" className="form-control" placeholder="10001" value={locZip} onChange={(e) => setLocZip(e.target.value)} />
                            </div>
                        </div>
                    </div>

                    {/*  Event Content Form  */}
                    <div id="content-event" className={`type-content ${activeTab === "event" ? "" : "d-none"}`}>
                        <div className="form-group mb-2">
                            <label htmlFor="event_name" className="text-muted mb-1">Event Name</label>
                            <input type="text" id="event_name" className="form-control" value={eventName} onChange={(e) => setEventName(e.target.value)} />
                        </div>
                        <div className="form-group mb-2">
                            <label htmlFor="event_loc" className="text-muted mb-1">Location</label>
                            <input type="text" id="event_loc" className="form-control" value={eventLoc} onChange={(e) => setEventLoc(e.target.value)} />
                        </div>
                        <div className="row">
                            <div className="col-md-6 form-group mb-0">
                                <label htmlFor="event_start" className="text-muted mb-1">Start Time</label>
                                <input type="datetime-local" id="event_start" className="form-control" value={eventStart} onChange={(e) => setEventStart(e.target.value)} />
                            </div>
                            <div className="col-md-6 form-group mb-0">
                                <label htmlFor="event_end" className="text-muted mb-1">End Time</label>
                                <input type="datetime-local" id="event_end" className="form-control" value={eventEnd} onChange={(e) => setEventEnd(e.target.value)} />
                            </div>
                        </div>
                    </div>

                    </div>
                    {/* Bulk Mode Upload - shared across all tabs */}
                    <div className={isBulk ? "" : "d-none"}>
                        <div id="drop-zone" className="drop-zone py-5">
                            <p className="mb-1 text-primary"><i className="fas fa-cloud-upload-alt fa-2x"></i></p>
                            <p className="mb-2 font-weight-bold">Drag & Drop CSV Here</p>
                            <p className="text-muted small mb-3">or</p>
                            <button className="btn btn-sm btn-outline" id="browse-btn" onClick={() => document.getElementById("csv-file").click()}>Browse Files</button>
                            <input type="file" id="csv-file" accept=".csv" style={{ display: "none" }} onChange={onFileUpload} />
                        </div>
                        <div className="text-center mt-3">
                            <a href={`./sample_${activeTab}.csv`} download={`sample_${activeTab}.csv`} className="text-muted">Download Sample CSV Format</a>
                        </div>
                        <div id="bulk-error-message" className="text-danger mt-2 text-center"></div>
                    </div>
                </div>
            </div>

            {/*  2. Set Colors  */}
            <div className={`card mb-3 p-0 overflow-hidden ${isBulk ? 'd-none' : ''}`}>
                <div className="card-header bg-transparent-glass-header d-flex justify-content-between align-items-center p-3 cursor-pointer" style={{ borderBottom: '1px solid var(--border-color)', cursor: 'pointer' }} onClick={() => setIsColorOpen(!isColorOpen)}>
                    <h5 className="mb-0">2. Set Colors</h5>
                    <i className={`fas ${isColorOpen ? 'fa-chevron-up' : 'fa-chevron-down'} text-muted`}></i>
                </div>
                <div className={`p-4 bg-transparent-glass ${isColorOpen ? '' : 'd-none'}`} id="color-section">
                    <div className="row">
                        <div className="col-md-6 form-group">
                            <label htmlFor="color_foreground" className="text-muted mb-2">Foreground Color</label>
                            <input type="color" id="color_foreground" name="color_foreground" className="form-control form-control-color w-100" value={fgColor} onChange={(e) => setFgColor(e.target.value)} style={{ height: '50px' }} />
                        </div>
                        <div className="col-md-6 form-group">
                            <label htmlFor="color_background" className="text-muted mb-2">Background Color</label>
                            <input type="color" id="color_background" name="color_background" className="form-control form-control-color w-100" value={bgColor} onChange={(e) => setBgColor(e.target.value)} style={{ height: '50px' }} />
                        </div>
                    </div>
                </div>
            </div>

            {/*  3. Add Logo Image  */}
            <div className={`card mb-3 p-0 overflow-hidden ${isBulk ? 'd-none' : ''}`}>
                <div className="card-header bg-transparent-glass-header d-flex justify-content-between align-items-center p-3 cursor-pointer" style={{ borderBottom: '1px solid var(--border-color)', cursor: 'pointer' }} onClick={() => setIsLogoOpen(!isLogoOpen)}>
                    <h5 className="mb-0">3. Add Logo Image</h5>
                    <i className={`fas ${isLogoOpen ? 'fa-chevron-up' : 'fa-chevron-down'} text-muted`}></i>
                </div>
                <div className={`p-4 bg-transparent-glass ${isLogoOpen ? '' : 'd-none'} border-start border-end border-bottom mb-2`} id="logo-section">
                    <div className="form-group mb-0">
                        <label htmlFor="logo_file" className="text-muted mb-2">Upload Logo (.png, .jpg)</label>
                        <input type="file" id="logo_file" name="logo_file" className="form-control" accept="image/png, image/jpeg" onChange={handleCenterLogoUpload} />
                        <small className="text-muted mt-1 d-block">A white margin will be added around the logo for readability.</small>
                        {centerLogo && (
                            <button className="btn btn-sm btn-outline-danger mt-2" onClick={() => { setCenterLogo(null); document.getElementById('logo_file').value = ''; }}>Remove Logo</button>
                        )}
                    </div>
                </div>
            </div>

            {/*  4. Customize Design  */}
            <div className={`card mb-3 p-0 overflow-hidden ${isBulk ? 'd-none' : ''}`}>
                <div className="card-header bg-transparent-glass-header d-flex justify-content-between align-items-center p-3 cursor-pointer" style={{ borderBottom: '1px solid var(--border-color)', cursor: 'pointer' }} onClick={() => setIsDesignOpen(!isDesignOpen)}>
                    <h5 className="mb-0">4. Customize Design</h5>
                    <i className={`fas ${isDesignOpen ? 'fa-chevron-up' : 'fa-chevron-down'} text-muted`}></i>
                </div>
                <div className={`p-4 bg-transparent-glass ${isDesignOpen ? '' : 'd-none'} border-start border-end border-bottom mb-2`} id="design-section">
                    <div className="mb-3">
                        <label htmlFor="body_shape" className="text-muted mb-2">Body Shape</label>
                        <select id="body_shape" className="form-select" value={bodyShape} onChange={(e) => setBodyShape(e.target.value)}>
                            <option value="square">Square</option>
                            <option value="dots">Dots</option>
                            <option value="rounded">Rounded</option>
                            <option value="extra-rounded">Extra Rounded</option>
                            <option value="classy">Classy</option>
                            <option value="classy-rounded">Classy Rounded</option>
                        </select>
                    </div>
                    <div className="mb-3">
                        <label htmlFor="eye_frame_shape" className="text-muted mb-2">Eye Frame Shape</label>
                        <select id="eye_frame_shape" className="form-select" value={eyeFrameShape} onChange={(e) => setEyeFrameShape(e.target.value)}>
                            <option value="square">Square</option>
                            <option value="dot">Dot</option>
                            <option value="extra-rounded">Extra Rounded</option>
                        </select>
                    </div>
                    <div className="mb-3">
                        <label htmlFor="eye_ball_shape" className="text-muted mb-2">Eye Ball Shape</label>
                        <select id="eye_ball_shape" className="form-select" value={eyeBallShape} onChange={(e) => setEyeBallShape(e.target.value)}>
                            <option value="square">Square</option>
                            <option value="dot">Dot</option>
                        </select>
                    </div>
                </div>
            </div>

        </div>

        {/*  Right Column: Preview & Action  */}
        <div className={`col-md-4 ${isBulk ? "d-none" : ""}`}>
            <div className="card p-3" style={{ position: 'sticky', top: '2rem', borderRadius: '0.5rem', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>
                {/*  Live Preview / Loading State  */}
                <div id="qr-preview-box" className={`qr-preview-box ${isBulk ? "d-none" : ""}`} style={{ minHeight: '250px', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f8fafc', borderRadius: '0.5rem', marginBottom: '1rem', border: '1px dashed var(--border-color)' }}>
                    <QRCodePreview 
                        data={getQrData()} 
                        fgColor={fgColor} 
                        bgColor={bgColor} 
                        bodyShape={bodyShape} eyeFrameShape={eyeFrameShape} eyeBallShape={eyeBallShape} 
                        logoFile={centerLogo} 
                    />
                </div>

                <button className={`btn btn-success btn-lg w-100 font-weight-bold ${isBulk ? "d-none" : ""}`} id="main-generate-btn">Create QR Code</button>
                
                <div id="download-actions"  className="mt-3">
                    <div className="d-flex gap-2">
                        <button className="btn btn-primary flex-grow-1" onClick={() => handleSingleDownload("png", getQrData(), fgColor, bgColor, bodyShape, eyeFrameShape, eyeBallShape, centerLogo)}>Download PNG</button>
                        <button className="btn btn-secondary flex-grow-1" onClick={() => handleSingleDownload("svg", getQrData(), fgColor, bgColor, bodyShape, eyeFrameShape, eyeBallShape, centerLogo)}>Download SVG</button>
                    </div>
                </div>

                {/*  Bulk Progress / Actions  */}
                <div id="bulk-progress-container" className={isBulk && bulkStage !== 'idle' ? "mt-4" : "d-none"}>
                    <p className="mb-2 text-center font-weight-bold">Generating QR Codes...</p>
                    <div className="progress-bar-bg">
                        <div className="progress-bar-fill" id="bulk-progress-fill" style={{ width: `${bulkProgress}%` }}></div>
                    </div>
                    <p className="text-center mt-2 text-muted" style={{ fontSize: '0.875rem' }} id="bulk-progress-text">{bulkProgress}% ({bulkRecords.filter(r => r.status === 'Valid').length} / {bulkRecords.filter(r => r.status === 'Valid').length})</p>
                </div>
            </div>
        </div>
    </div>

{/*  Modal for Bulk Preview & Results  */}

{/* Dynamic React Bulk Modal */}
{showBulkModal && (
    <div className="position-fixed w-100 h-100 d-flex" style={{ top: 0, left: 0, background: "rgba(0,0,0,0.6)", zIndex: 1050, alignItems: "center", justifyContent: "center" }}>
        <div className="bg-white rounded p-4 shadow-lg" style={{ width: '90%', maxWidth: '800px', maxHeight: '90vh', overflowY: 'auto', position: 'relative' }}>
            <button onClick={() => setShowBulkModal(false)} className="btn btn-sm btn-outline text-muted" style={{ position: 'absolute', top: '1rem', right: '1rem' }}>✕ Close</button>
            
            <h3 className="mb-3">Bulk CSV Preview</h3>
            
            {bulkStage === 'preview' && (
                <div>
                    <div className="d-flex justify-content-between align-items-center mb-3">
                        <span className="font-weight-bold">{bulkFilename}</span>
                        <span className="badge bg-secondary">Total: {bulkRecords.length} | Valid: {bulkRecords.filter(r => r.status === 'Valid').length}</span>
                    </div>
                    <div className="table-responsive" style={{ maxHeight: '300px' }}>
                        <table className="table table-sm">
                            <thead><tr><th>#</th><th>{bulkColumnConfig[activeTab]?.label || 'Data'}</th><th>Status</th></tr></thead>
                            <tbody>
                                {bulkRecords.map((r, i) => (
                                    <tr key={i}>
                                        <td>{r.index}</td>
                                        <td className="text-truncate" style={{maxWidth: '250px'}}>{r.display}</td>
                                        <td className={r.status === 'Valid' ? 'text-success' : 'text-danger'}>{r.status}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    <div className="d-flex gap-2 mt-4">
                        <select className="form-select w-auto" value={bulkFormat} onChange={(e) => setBulkFormat(e.target.value)}>
                            <option value="png">PNG</option>
                            <option value="svg">SVG</option>
                            <option value="jpeg">JPG</option>
                        </select>
                        <button className="btn btn-success flex-grow-1" onClick={startBulkGeneration}>Start Generation & Download ZIP</button>
                    </div>
                </div>
            )}

            {bulkStage === 'generating' && (
                <div className="text-center py-5">
                    <h4 className="mt-3">Generating ZIP...</h4>
                    <div className="progress mt-4" style={{height: '25px'}}>
                        <div className="progress-bar progress-bar-striped progress-bar-animated bg-success" style={{width: `${bulkProgress}%`}}>{bulkText}</div>
                    </div>
                </div>
            )}

            {bulkStage === 'done' && (
                <div className="text-center py-5">
                    <i className="fas fa-check-circle text-success" style={{fontSize: '4rem'}}></i>
                    <h4 className="mt-3">QR Codes Generated Successfully!</h4>
                    <p className="text-muted">Your ZIP file has been downloaded.</p>
                </div>
            )}
        </div>
    </div>
)}

        </div>
        </div>
    );
}
