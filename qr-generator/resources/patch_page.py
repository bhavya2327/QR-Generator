import re

with open('src/app/page.js', 'r') as f:
    code = f.read()

# Add states for all types
states = """
    // Tab State
    const [activeTab, setActiveTab] = useState('url');
    const [isBulk, setIsBulk] = useState(false);
    
    // Core Generation States
    const [fgColor, setFgColor] = useState('#000000');
    const [bgColor, setBgColor] = useState('#ffffff');
    const [styleShape, setStyleShape] = useState('square');

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
    const [vcardJob, setVcardJob] = useState('');
    const [vcardStreet, setVcardStreet] = useState('');
    const [vcardCity, setVcardCity] = useState('');
    const [vcardZip, setVcardZip] = useState('');
    const [vcardState, setVcardState] = useState('');
    const [vcardCountry, setVcardCountry] = useState('');
    const [vcardWebsite, setVcardWebsite] = useState('');
    
    // WiFi
    const [wifiName, setWifiName] = useState('');
    const [wifiPass, setWifiPass] = useState('');
    const [wifiEnc, setWifiEnc] = useState('WPA');

    const getQrData = () => {
        if (activeTab === 'url') return url || 'https://example.com';
        if (activeTab === 'text') return text || 'Text';
        if (activeTab === 'email') return `MATMSG:TO:${email};SUB:${emailSub};BODY:${emailBody};;`;
        if (activeTab === 'phone') return `tel:${phone}`;
        if (activeTab === 'sms') return `smsto:${smsNumber}:${smsMessage}`;
        if (activeTab === 'vcard') {
            return `BEGIN:VCARD\\nVERSION:3.0\\nN:${vcardLast};${vcardFirst}\\nFN:${vcardFirst} ${vcardLast}\\nORG:${vcardCompany}\\nTITLE:${vcardJob}\\nTEL;TYPE=work,voice:${vcardPhone}\\nTEL;TYPE=cell,voice:${vcardMobile}\\nTEL;TYPE=fax:${vcardFax}\\nEMAIL:${vcardEmail}\\nURL:${vcardWebsite}\\nADR;TYPE=work:;;${vcardStreet};${vcardCity};${vcardState};${vcardZip};${vcardCountry}\\nEND:VCARD`;
        }
        if (activeTab === 'wifi') return `WIFI:S:${wifiName};T:${wifiEnc};P:${wifiPass};;`;
        return 'https://example.com';
    };
"""

# Replace top states
code = re.sub(r'const \[activeTab.*?const \[styleShape, setStyleShape\] = useState\(\'square\'\);', states, code, flags=re.DOTALL)

# Wire up tabs onClick
code = re.sub(r'<button className="btn btn-primary type-btn active" data-type="url"', r'<button className={`btn type-btn ${activeTab === "url" ? "btn-primary active" : "btn-outline"}`} onClick={() => setActiveTab("url")}', code)
for tab in ['text', 'email', 'phone', 'sms', 'vcard', 'wifi']:
    code = re.sub(f'<button className="btn btn-outline type-btn" data-type="{tab}"', f'<button className={{`btn type-btn ${{activeTab === "{tab}" ? "btn-primary active" : "btn-outline"}}`}} onClick={{() => setActiveTab("{tab}")}}', code)

# Hide/Show tab contents based on state
for tab in ['url', 'text', 'email', 'phone', 'sms', 'vcard', 'wifi']:
    code = code.replace(f'<div id="content-{tab}" className="type-content"', f'<div id="content-{tab}" className={{`type-content ${{activeTab === "{tab}" ? "" : "d-none"}}`}}')

# Replace form inputs with value/onChange
replacements = [
    (r'<textarea name="text" id="text_content" className="form-control" rows="4" required></textarea>', r'<textarea name="text" id="text_content" className="form-control" rows="4" required value={text} onChange={(e) => setText(e.target.value)}></textarea>'),
    (r'<input type="email" name="email_to" id="email_to" className="form-control" placeholder="example@email.com" required />', r'<input type="email" name="email_to" id="email_to" className="form-control" placeholder="example@email.com" required value={email} onChange={(e) => setEmail(e.target.value)} />'),
    (r'<input type="text" name="email_sub" id="email_sub" className="form-control" placeholder="Subject" />', r'<input type="text" name="email_sub" id="email_sub" className="form-control" placeholder="Subject" value={emailSub} onChange={(e) => setEmailSub(e.target.value)} />'),
    (r'<textarea name="email_body" id="email_body" className="form-control" rows="3" placeholder="Message body"></textarea>', r'<textarea name="email_body" id="email_body" className="form-control" rows="3" placeholder="Message body" value={emailBody} onChange={(e) => setEmailBody(e.target.value)}></textarea>'),
    (r'<input type="tel" name="phone" id="phone_number" className="form-control" placeholder="+1234567890" required />', r'<input type="tel" name="phone" id="phone_number" className="form-control" placeholder="+1234567890" required value={phone} onChange={(e) => setPhone(e.target.value)} />'),
    (r'<input type="tel" name="sms_to" id="sms_to" className="form-control" placeholder="+1234567890" required />', r'<input type="tel" name="sms_to" id="sms_to" className="form-control" placeholder="+1234567890" required value={smsNumber} onChange={(e) => setSmsNumber(e.target.value)} />'),
    (r'<textarea name="sms_body" id="sms_body" className="form-control" rows="3" placeholder="Your message"></textarea>', r'<textarea name="sms_body" id="sms_body" className="form-control" rows="3" placeholder="Your message" value={smsMessage} onChange={(e) => setSmsMessage(e.target.value)}></textarea>'),
    
    # vCard
    (r'<input type="text" name="v_first" id="v_first" className="form-control" />', r'<input type="text" className="form-control" value={vcardFirst} onChange={(e) => setVcardFirst(e.target.value)} />'),
    (r'<input type="text" name="v_last" id="v_last" className="form-control" />', r'<input type="text" className="form-control" value={vcardLast} onChange={(e) => setVcardLast(e.target.value)} />'),
    (r'<input type="tel" name="v_mobile" id="v_mobile" className="form-control" />', r'<input type="tel" className="form-control" value={vcardMobile} onChange={(e) => setVcardMobile(e.target.value)} />'),
    (r'<input type="tel" name="v_phone" id="v_phone" className="form-control" />', r'<input type="tel" className="form-control" value={vcardPhone} onChange={(e) => setVcardPhone(e.target.value)} />'),
    (r'<input type="tel" name="v_fax" id="v_fax" className="form-control" />', r'<input type="tel" className="form-control" value={vcardFax} onChange={(e) => setVcardFax(e.target.value)} />'),
    (r'<input type="email" name="v_email" id="v_email" className="form-control" />', r'<input type="email" className="form-control" value={vcardEmail} onChange={(e) => setVcardEmail(e.target.value)} />'),
    (r'<input type="text" name="v_company" id="v_company" className="form-control" />', r'<input type="text" className="form-control" value={vcardCompany} onChange={(e) => setVcardCompany(e.target.value)} />'),
    (r'<input type="text" name="v_job" id="v_job" className="form-control" />', r'<input type="text" className="form-control" value={vcardJob} onChange={(e) => setVcardJob(e.target.value)} />'),
    (r'<input type="text" name="v_street" id="v_street" className="form-control" />', r'<input type="text" className="form-control" value={vcardStreet} onChange={(e) => setVcardStreet(e.target.value)} />'),
    (r'<input type="text" name="v_city" id="v_city" className="form-control" />', r'<input type="text" className="form-control" value={vcardCity} onChange={(e) => setVcardCity(e.target.value)} />'),
    (r'<input type="text" name="v_zip" id="v_zip" className="form-control" />', r'<input type="text" className="form-control" value={vcardZip} onChange={(e) => setVcardZip(e.target.value)} />'),
    (r'<input type="text" name="v_state" id="v_state" className="form-control" />', r'<input type="text" className="form-control" value={vcardState} onChange={(e) => setVcardState(e.target.value)} />'),
    (r'<input type="text" name="v_country" id="v_country" className="form-control" />', r'<input type="text" className="form-control" value={vcardCountry} onChange={(e) => setVcardCountry(e.target.value)} />'),
    (r'<input type="url" name="v_www" id="v_www" className="form-control" />', r'<input type="url" className="form-control" value={vcardWebsite} onChange={(e) => setVcardWebsite(e.target.value)} />'),

    # WiFi
    (r'<input type="text" name="wifi_ssid" id="wifi_ssid" className="form-control" required />', r'<input type="text" className="form-control" required value={wifiName} onChange={(e) => setWifiName(e.target.value)} />'),
    (r'<input type="text" name="wifi_pass" id="wifi_pass" className="form-control" />', r'<input type="text" className="form-control" value={wifiPass} onChange={(e) => setWifiPass(e.target.value)} />'),
    (r'<select id="wifi_encryption" name="wifi_encryption" className="form-control">', r'<select id="wifi_encryption" name="wifi_encryption" className="form-control" value={wifiEnc} onChange={(e) => setWifiEnc(e.target.value)}>')
]

for src, dst in replacements:
    code = code.replace(src, dst)

# Update Preview
code = re.sub(r'data={url}', r'data={getQrData()}', code)

with open('src/app/page.js', 'w') as f:
    f.write(code)

print("success")
