import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# 1. Update State
state_old = """    // Location
    const [lat, setLat] = useState('');
    const [lng, setLng] = useState('');"""
state_new = """    // Location
    const [locStreet, setLocStreet] = useState('');
    const [locCity, setLocCity] = useState('');
    const [locState, setLocState] = useState('');
    const [locZip, setLocZip] = useState('');"""
text = text.replace(state_old, state_new)

# 2. Update getQrData()
getdata_old = """        if (activeTab === 'location') return `geo:${lat},${lng}`;"""
getdata_new = """        if (activeTab === 'location') {
            const query = encodeURIComponent(`${locStreet} ${locCity} ${locState} ${locZip}`.trim());
            return query ? `https://www.google.com/maps/search/?api=1&query=${query}` : 'https://www.google.com/maps';
        }"""
text = text.replace(getdata_old, getdata_new)

# 3. Update Form
form_old = """                    {/*  Location Content Form  */}
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
                    </div>"""

form_new = """                    {/*  Location Content Form  */}
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
                    </div>"""
text = text.replace(form_old, form_new)


with open('src/app/page.js', 'w') as f:
    f.write(text)

