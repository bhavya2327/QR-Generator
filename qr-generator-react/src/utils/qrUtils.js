import QRCodeStyling from 'qr-code-styling';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import Papa from 'papaparse';

export const handleSingleDownload = (format, data, fgColor, bgColor, bodyShape, eyeFrameShape, eyeBallShape, logoFile) => {
    const qrCode = new QRCodeStyling({
        width: 300,
        height: 300,
        type: "svg",
        data: data || "https://example.com",
        image: logoFile,
        qrOptions: { errorCorrectionLevel: 'H' },
        dotsOptions: {
            color: fgColor,
            type: bodyShape
        },
        cornersSquareOptions: {
            color: fgColor,
            type: eyeFrameShape
        },
        cornersDotOptions: {
            color: fgColor,
            type: eyeBallShape
        },
        backgroundOptions: { color: bgColor },
        imageOptions: { crossOrigin: "anonymous", margin: 5, imageSize: 0.4 }
    });

    qrCode.download({ name: "qr-code", extension: format });
};

export const processBulkCSV = (file, fgColor, bgColor, styleShape, logoFile, onProgress) => {
    return new Promise((resolve, reject) => {
        Papa.parse(file, {
            header: false,
            skipEmptyLines: true,
            complete: async (results) => {
                const zip = new JSZip();
                const rows = results.data;
                const total = rows.length;

                for (let i = 0; i < total; i++) {
                    const url = rows[i][0];
                    if (!url) continue;

                    const qrCode = new QRCodeStyling({
                        width: 300,
                        height: 300,
                        type: "svg",
                        data: url,
                        image: logoFile,
                        dotsOptions: {
                            color: fgColor,
                            type: styleShape === 'dot' ? 'dots' : styleShape === 'round' ? 'rounded' : 'square'
                        },
                        backgroundOptions: { color: bgColor },
                        imageOptions: { crossOrigin: "anonymous", margin: 5 }
                    });

                    // We need to wait for rendering to blob to add it to zip
                    const blob = await qrCode.getRawData("png");
                    if (blob) {
                        zip.file(`qr-${i + 1}.png`, blob);
                    }
                    
                    onProgress(Math.round(((i + 1) / total) * 100), i + 1, total);
                }

                zip.generateAsync({ type: "blob" }).then((content) => {
                    saveAs(content, "bulk-qrs.zip");
                    resolve();
                });
            },
            error: (err) => reject(err)
        });
    });
};
