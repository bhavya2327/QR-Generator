import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# 1. Remove the "coming soon" placeholders completely
text = re.sub(r'<div id="content-location".*?</div>\n?', '', text)
text = re.sub(r'<div id="content-event".*?</div>\n?', '', text)
text = re.sub(r'<div id="content-crypto".*?</div>\n?', '', text)

# 2. Add vcardDesc state
state_block = """    const [vcardCompany, setVcardCompany] = useState('');"""
new_state_block = """    const [vcardCompany, setVcardCompany] = useState('');
    const [vcardDesc, setVcardDesc] = useState('');"""
text = text.replace(state_block, new_state_block)

# 3. Add vcardDesc to the form UI
vcard_ui = """                            <div className="col-md-12 form-group mb-0">
                                <label htmlFor="vcard_company" className="text-muted mb-1">Company</label>
                                <input type="text" id="vcard_company" name="vcard_company" className="form-control" value={vcardCompany} onChange={(e) => setVcardCompany(e.target.value)} />
                            </div>"""
new_vcard_ui = """                            <div className="col-md-12 form-group mb-2">
                                <label htmlFor="vcard_company" className="text-muted mb-1">Company</label>
                                <input type="text" id="vcard_company" name="vcard_company" className="form-control" value={vcardCompany} onChange={(e) => setVcardCompany(e.target.value)} />
                            </div>
                            <div className="col-md-12 form-group mb-0">
                                <label htmlFor="vcard_desc" className="text-muted mb-1">Description</label>
                                <textarea id="vcard_desc" name="vcard_desc" className="form-control" rows="3" value={vcardDesc} onChange={(e) => setVcardDesc(e.target.value)}></textarea>
                            </div>"""
text = text.replace(vcard_ui, new_vcard_ui)

# 4. Add vcardDesc to getQrData()
# The vCard format is:
"""
        if (activeTab === 'vcard') {
            return `BEGIN:VCARD
VERSION:3.0
N:${vcardLast};${vcardFirst}
FN:${vcardFirst} ${vcardLast}
ORG:${vcardCompany}
TITLE:${vcardJob}
"""
vcard_data_old = """ORG:${vcardCompany}
TITLE:${vcardJob}"""
vcard_data_new = """ORG:${vcardCompany}
TITLE:${vcardJob}
NOTE:${vcardDesc}"""
text = text.replace(vcard_data_old, vcard_data_new)

with open('src/app/page.js', 'w') as f:
    f.write(text)

