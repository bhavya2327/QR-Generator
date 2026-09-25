import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# Remove style={{ display: 'none' }} from type-content divs
text = text.replace("""style={{ display: 'none' }}""", "")

# Add React state bindings to inputs
# 1. Text
text = text.replace("""<textarea id="text" name="text" className="form-control" rows="4" placeholder="Enter your text here..."></textarea>""",
                    """<textarea id="text" name="text" className="form-control" rows="4" placeholder="Enter your text here..." value={text} onChange={(e) => setText(e.target.value)}></textarea>""")

# 2. Email
text = text.replace("""<input type="email" id="email" name="email" className="form-control" placeholder="your@email.com" />""",
                    """<input type="email" id="email" name="email" className="form-control" placeholder="your@email.com" value={email} onChange={(e) => setEmail(e.target.value)} />""")
text = text.replace("""<input type="text" id="email_subject" name="email_subject" className="form-control" placeholder="Subject" />""",
                    """<input type="text" id="email_subject" name="email_subject" className="form-control" placeholder="Subject" value={emailSub} onChange={(e) => setEmailSub(e.target.value)} />""")
text = text.replace("""<textarea id="email_body" name="email_body" className="form-control" rows="3"></textarea>""",
                    """<textarea id="email_body" name="email_body" className="form-control" rows="3" value={emailBody} onChange={(e) => setEmailBody(e.target.value)}></textarea>""")

# 3. Phone
text = text.replace("""<input type="tel" id="phone" name="phone" className="form-control" placeholder="+1234567890" />""",
                    """<input type="tel" id="phone" name="phone" className="form-control" placeholder="+1234567890" value={phone} onChange={(e) => setPhone(e.target.value)} />""")

# 4. SMS
text = text.replace("""<input type="tel" id="sms_phone" name="sms_phone" className="form-control" placeholder="+1234567890" />""",
                    """<input type="tel" id="sms_phone" name="sms_phone" className="form-control" placeholder="+1234567890" value={smsNumber} onChange={(e) => setSmsNumber(e.target.value)} />""")
text = text.replace("""<textarea id="sms_message" name="sms_message" className="form-control" rows="3"></textarea>""",
                    """<textarea id="sms_message" name="sms_message" className="form-control" rows="3" value={smsMessage} onChange={(e) => setSmsMessage(e.target.value)}></textarea>""")

# 5. vCard
text = text.replace("""<input type="text" id="vcard_first_name" name="vcard_first_name" className="form-control" />""",
                    """<input type="text" id="vcard_first_name" name="vcard_first_name" className="form-control" value={vcardFirst} onChange={(e) => setVcardFirst(e.target.value)} />""")
text = text.replace("""<input type="text" id="vcard_last_name" name="vcard_last_name" className="form-control" />""",
                    """<input type="text" id="vcard_last_name" name="vcard_last_name" className="form-control" value={vcardLast} onChange={(e) => setVcardLast(e.target.value)} />""")
text = text.replace("""<input type="text" id="vcard_phone" name="vcard_phone" className="form-control" />""",
                    """<input type="text" id="vcard_phone" name="vcard_phone" className="form-control" value={vcardPhone} onChange={(e) => setVcardPhone(e.target.value)} />""")
text = text.replace("""<input type="email" id="vcard_email" name="vcard_email" className="form-control" />""",
                    """<input type="email" id="vcard_email" name="vcard_email" className="form-control" value={vcardEmail} onChange={(e) => setVcardEmail(e.target.value)} />""")
text = text.replace("""<input type="text" id="vcard_company" name="vcard_company" className="form-control" />""",
                    """<input type="text" id="vcard_company" name="vcard_company" className="form-control" value={vcardCompany} onChange={(e) => setVcardCompany(e.target.value)} />""")

# 6. WiFi
text = text.replace("""<input type="text" id="wifi_ssid" name="wifi_ssid" className="form-control" />""",
                    """<input type="text" id="wifi_ssid" name="wifi_ssid" className="form-control" value={wifiName} onChange={(e) => setWifiName(e.target.value)} />""")
text = text.replace("""<input type="text" id="wifi_password" name="wifi_password" className="form-control" />""",
                    """<input type="text" id="wifi_password" name="wifi_password" className="form-control" value={wifiPass} onChange={(e) => setWifiPass(e.target.value)} />""")

with open('src/app/page.js', 'w') as f:
    f.write(text)

