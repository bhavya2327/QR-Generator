import re

with open('src/app/page.js', 'r') as f:
    text = f.read()

# First let's remove the OLD bulk state if it's there
text = re.sub(r'const \[isBulkProcessing, setIsBulkProcessing\] = useState\(false\);.*?setIsBulkProcessing\(false\);\n    };', '', text, flags=re.DOTALL)

# Insert the proper state just before return (
new_bulk_state = """
    const [isBulkProcessing, setIsBulkProcessing] = useState(false);
    const [bulkProgress, setBulkProgress] = useState(0);
    const [bulkText, setBulkText] = useState('');
    
    // New states for the Bulk Preview Modal
    const [showBulkModal, setShowBulkModal] = useState(false);
    const [bulkRecords, setBulkRecords] = useState([]);
    const [bulkFilename, setBulkFilename] = useState('');
    const [bulkStage, setBulkStage] = useState('preview'); // 'preview' | 'generating' | 'done'
    const [bulkFormat, setBulkFormat] = useState('png');

    const onFileUpload = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        setBulkFilename(file.name);
        
        import('papaparse').then((Papa) => {
            Papa.default.parse(file, {
                header: false,
                skipEmptyLines: true,
                complete: (results) => {
                    const records = results.data.map((row, idx) => ({
                        index: idx + 1,
                        url: row[0],
                        status: row[0] && row[0].startsWith('http') ? 'Valid' : 'Invalid'
                    }));
                    setBulkRecords(records);
                    setBulkStage('preview');
                    setShowBulkModal(true);
                }
            });
        });
    };

    const startBulkGeneration = async () => {
        const validUrls = bulkRecords.filter(r => r.status === 'Valid').map(r => r.url);
        if (validUrls.length === 0) return alert('No valid URLs found.');
        
        setBulkStage('generating');
        
        try {
            const JSZip = (await import('jszip')).default;
            const QRCodeStyling = (await import('qr-code-styling')).default;
            const zip = new JSZip();
            const total = validUrls.length;

            for (let i = 0; i < total; i++) {
                const url = validUrls[i];
                const qrCode = new QRCodeStyling({
                    width: 300, height: 300, type: "svg", data: url,
                    dotsOptions: { color: fgColor, type: styleShape === 'dot' ? 'dots' : styleShape === 'round' ? 'rounded' : 'square' },
                    backgroundOptions: { color: bgColor }
                });

                const blob = await qrCode.getRawData(bulkFormat);
                if (blob) zip.file(`qr-${i + 1}.${bulkFormat}`, blob);
                
                setBulkProgress(Math.round(((i + 1) / total) * 100));
                setBulkText(`${Math.round(((i + 1) / total) * 100)}% (${i + 1} / ${total})`);
            }

            const content = await zip.generateAsync({ type: "blob" });
            const { saveAs } = await import('file-saver');
            saveAs(content, `bulk-qrs-${bulkFormat}.zip`);
            
            setBulkStage('done');
        } catch(e) {
            console.error(e);
            alert('Failed to process bulk CSV.');
            setShowBulkModal(false);
        }
    };
"""

text = text.replace('return (', new_bulk_state + '\n    return (')

with open('src/app/page.js', 'w') as f:
    f.write(text)

print("State inserted")
