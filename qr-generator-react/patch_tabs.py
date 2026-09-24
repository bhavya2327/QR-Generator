import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# 1. Remove WiFi and Crypto buttons
text = re.sub(r'<button className=\{`btn type-btn \$\{activeTab === "wifi" \? "btn-primary active" : "btn-outline"\}`\} onClick=\{.*?\}><i className="fas fa-wifi"></i> WiFi</button>\n?', '', text)
text = re.sub(r'<button className="btn btn-outline type-btn" data-type="crypto"><i className="fab fa-bitcoin"></i> Crypto</button>\n?', '', text)

# 2. Fix Event and Location buttons to use onClick like the rest
text = text.replace("""<button className="btn btn-outline type-btn" data-type="location"><i className="fas fa-map-marker-alt"></i> Location</button>""",
                    """<button className={`btn type-btn ${activeTab === "location" ? "btn-primary active" : "btn-outline"}`} onClick={() => setActiveTab("location")}><i className="fas fa-map-marker-alt"></i> Location</button>""")

text = text.replace("""<button className="btn btn-outline type-btn" data-type="event"><i className="fas fa-calendar-alt"></i> Event</button>""",
                    """<button className={`btn type-btn ${activeTab === "event" ? "btn-primary active" : "btn-outline"}`} onClick={() => setActiveTab("event")}><i className="fas fa-calendar-alt"></i> Event</button>""")

# 3. Add state variables for Location and Event, remove WiFi
state_old = """    // WiFi
    const [wifiName, setWifiName] = useState('');
    const [wifiPass, setWifiPass] = useState('');
    const [wifiEnc, setWifiEnc] = useState('WPA');"""
    
state_new = """    // Location
    const [lat, setLat] = useState('');
    const [lng, setLng] = useState('');

    // Event
    const [eventName, setEventName] = useState('');
    const [eventLoc, setEventLoc] = useState('');
    const [eventStart, setEventStart] = useState('');
    const [eventEnd, setEventEnd] = useState('');"""
text = text.replace(state_old, state_new)

# 4. Remove WiFi from getQrData, add Location and Event
getdata_old = """        if (activeTab === 'wifi') return `WIFI:S:${wifiName};T:${wifiEnc};P:${wifiPass};;`;"""
getdata_new = """        if (activeTab === 'location') return `geo:${lat},${lng}`;
        if (activeTab === 'event') {
            const formatDT = (dt) => dt ? dt.replace(/[-:]/g, '') + 'Z' : '';
            return `BEGIN:VEVENT\\nSUMMARY:${eventName}\\nLOCATION:${eventLoc}\\nDTSTART:${formatDT(eventStart)}\\nDTEND:${formatDT(eventEnd)}\\nEND:VEVENT`;
        }"""
text = text.replace(getdata_old, getdata_new)

# 5. Remove WiFi form
text = re.sub(r'<!--\s*WiFi Content Form\s*-->.*?(?=<!--)', '', text, flags=re.DOTALL)
text = re.sub(r'\{\/\*  WiFi Content Form  \*\/\}.*?</div>\n                    </div>', '', text, flags=re.DOTALL)

# 6. Add Location and Event Forms
forms_to_add = """                    {/*  Location Content Form  */}
                    <div id="content-location" className={`type-content ${activeTab === "location" ? "" : "d-none"}`}>
                        <div className="row">
                            <div className="col-md-6 form-group mb-0">
                                <label htmlFor="loc_lat" className="text-muted mb-1">Latitude</label>
                                <input type="number" step="any" id="loc_lat" className="form-control" placeholder="40.7128" value={lat} onChange={(e) => setLat(e.target.value)} />
                            </div>
                            <div className="col-md-6 form-group mb-0">
                                <label htmlFor="loc_lng" className="text-muted mb-1">Longitude</label>
                                <input type="number" step="any" id="loc_lng" className="form-control" placeholder="-74.0060" value={lng} onChange={(e) => setLng(e.target.value)} />
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
                    </div>"""

# Insert right after vCard form
vcard_end = """                            <div className="col-md-12 form-group mb-0">
                                <label htmlFor="vcard_desc" className="text-muted mb-1">Description</label>
                                <textarea id="vcard_desc" name="vcard_desc" className="form-control" rows="3" value={vcardDesc} onChange={(e) => setVcardDesc(e.target.value)}></textarea>
                            </div>
                        </div>
                    </div>"""

text = text.replace(vcard_end, vcard_end + "\n\n" + forms_to_add)

with open('src/app/page.js', 'w') as f:
    f.write(text)

