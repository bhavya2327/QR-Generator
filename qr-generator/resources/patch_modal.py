import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# Hide bulk modal by default, and change style to React format
text = text.replace('<div id="bulk-modal" className="position-fixed w-100 h-100" style="">', '<div id="bulk-modal" className={`position-fixed w-100 h-100 ${isBulkProcessing ? "d-flex" : "d-none"}`} style={{ top: 0, left: 0, background: "rgba(0,0,0,0.6)", zIndex: 1050, alignItems: "center", justifyContent: "center" }}>')
text = text.replace('<div id="bulk-modal" className="position-fixed w-100 h-100">', '<div id="bulk-modal" className={`position-fixed w-100 h-100 ${isBulkProcessing ? "d-flex" : "d-none"}`} style={{ top: 0, left: 0, background: "rgba(0,0,0,0.6)", zIndex: 1050, alignItems: "center", justifyContent: "center" }}>')

text = text.replace('<div className="bg-white rounded shadow-lg p-4" style="">', '<div className="bg-white rounded shadow-lg p-4" style={{ width: "90%", maxWidth: "800px", maxHeight: "90vh", overflowY: "auto", position: "relative" }}>')
text = text.replace('<div className="bg-white rounded shadow-lg p-4">', '<div className="bg-white rounded shadow-lg p-4" style={{ width: "90%", maxWidth: "800px", maxHeight: "90vh", overflowY: "auto", position: "relative" }}>')

# Remove @csrf completely from file (it was partially removed earlier with sed but just in case)
text = text.replace('@csrf', '')

# Accordion sections need cursor-pointer and borders
text = text.replace('<div className="bg-white p-3 rounded mb-2 border cursor-pointer font-weight-bold" onClick={() => {}} >', '<div className="bg-white p-3 rounded mb-2 border cursor-pointer font-weight-bold" style={{ cursor: "pointer" }} onClick={() => document.getElementById("colors-section").classList.toggle("d-none")}>')
text = text.replace('<div className="bg-white p-3 rounded mb-2 border cursor-pointer font-weight-bold" onClick={() => {}}>', '<div className="bg-white p-3 rounded mb-2 border cursor-pointer font-weight-bold" style={{ cursor: "pointer" }} onClick={() => document.getElementById("colors-section").classList.toggle("d-none")}>')

with open('src/app/page.js', 'w') as f:
    f.write(text)
