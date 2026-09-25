import re

with open('src/app/page.js', 'r') as f:
    content = f.read()

# 1. Wrap the container
content = content.replace('<div className="container mt-4 mb-5">', 
'''<div className="container mt-5 mb-5 p-4 p-md-5 bg-white shadow-sm" style={{ borderRadius: '24px', maxWidth: '1100px' }}>''', 1)

# 2. Rewrite the tabs
tabs_pattern = r'<div className="d-flex overflow-auto pb-2 mb-4" id="type-tabs" >(.*?)</div>'
tabs_replacement = r'''<div className="d-flex gap-2 overflow-auto pb-3 mb-4" id="type-tabs" >
        <button className={`btn d-flex align-items-center gap-2 fw-medium px-3 py-2 border-0 ${activeTab === "url" ? "" : "text-muted bg-transparent"}`} style={{ backgroundColor: activeTab === "url" ? "#f4f4f5" : "transparent", borderRadius: "12px" }} onClick={() => setActiveTab("url")}><i className="fas fa-link"></i> URL</button>
        <button className={`btn d-flex align-items-center gap-2 fw-medium px-3 py-2 border-0 ${activeTab === "text" ? "" : "text-muted bg-transparent"}`} style={{ backgroundColor: activeTab === "text" ? "#f4f4f5" : "transparent", borderRadius: "12px" }} onClick={() => setActiveTab("text")}><i className="fas fa-font"></i> Text</button>
        <button className={`btn d-flex align-items-center gap-2 fw-medium px-3 py-2 border-0 ${activeTab === "email" ? "" : "text-muted bg-transparent"}`} style={{ backgroundColor: activeTab === "email" ? "#f4f4f5" : "transparent", borderRadius: "12px" }} onClick={() => setActiveTab("email")}><i className="fas fa-envelope"></i> Email</button>
        <button className={`btn d-flex align-items-center gap-2 fw-medium px-3 py-2 border-0 ${activeTab === "phone" ? "" : "text-muted bg-transparent"}`} style={{ backgroundColor: activeTab === "phone" ? "#f4f4f5" : "transparent", borderRadius: "12px" }} onClick={() => setActiveTab("phone")}><i className="fas fa-phone"></i> Phone</button>
        <button className={`btn d-flex align-items-center gap-2 fw-medium px-3 py-2 border-0 ${activeTab === "sms" ? "" : "text-muted bg-transparent"}`} style={{ backgroundColor: activeTab === "sms" ? "#f4f4f5" : "transparent", borderRadius: "12px" }} onClick={() => setActiveTab("sms")}><i className="fas fa-comment"></i> SMS</button>
        <button className={`btn d-flex align-items-center gap-2 fw-medium px-3 py-2 border-0 ${activeTab === "vcard" ? "" : "text-muted bg-transparent"}`} style={{ backgroundColor: activeTab === "vcard" ? "#f4f4f5" : "transparent", borderRadius: "12px" }} onClick={() => setActiveTab("vcard")}><i className="fas fa-id-card"></i> vCard</button>
        <button className={`btn d-flex align-items-center gap-2 fw-medium px-3 py-2 border-0 ${activeTab === "smartcard" ? "" : "text-muted bg-transparent"}`} style={{ backgroundColor: activeTab === "smartcard" ? "#f4f4f5" : "transparent", borderRadius: "12px" }} onClick={() => setActiveTab("smartcard")}><i className="fas fa-id-badge"></i> Smart Card</button>
        <button className={`btn d-flex align-items-center gap-2 fw-medium px-3 py-2 border-0 ${activeTab === "location" ? "" : "text-muted bg-transparent"}`} style={{ backgroundColor: activeTab === "location" ? "#f4f4f5" : "transparent", borderRadius: "12px" }} onClick={() => setActiveTab("location")}><i className="fas fa-map-marker-alt"></i> Location</button>
        <button className={`btn d-flex align-items-center gap-2 fw-medium px-3 py-2 border-0 ${activeTab === "event" ? "" : "text-muted bg-transparent"}`} style={{ backgroundColor: activeTab === "event" ? "#f4f4f5" : "transparent", borderRadius: "12px" }} onClick={() => setActiveTab("event")}><i className="fas fa-calendar-alt"></i> Event</button>
    </div>'''
content = re.sub(tabs_pattern, tabs_replacement, content, flags=re.DOTALL)

with open('src/app/page.js', 'w') as f:
    f.write(content)
