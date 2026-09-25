import fs from 'fs';
import QRCodeStyling from 'qr-code-styling-node';
import { createCanvas } from 'canvas';

// Create a dummy image
const canvas = createCanvas(64, 64);
const ctx = canvas.getContext('2d');
ctx.fillStyle = 'red';
ctx.fillRect(0, 0, 64, 64);
const dataUrl = canvas.toDataURL('image/jpeg', 0.2);
const base64 = dataUrl.split(',')[1];

let foldedBase64 = 'PHOTO;ENCODING=b;TYPE=JPEG:';
let currentLineLength = foldedBase64.length;
for (let i = 0; i < base64.length; i++) {
    foldedBase64 += base64[i];
    currentLineLength++;
    if (currentLineLength >= 75 && i !== base64.length - 1) {
        foldedBase64 += '\r\n ';
        currentLineLength = 1;
    }
}

const vcard = `BEGIN:VCARD
VERSION:3.0
N:Doe;John
FN:John Doe
ORG:Company
TITLE:Developer
NOTE:Notes
${foldedBase64}
TEL;TYPE=work,voice:1234567890
EMAIL:john@example.com
END:VCARD`;

console.log("vCard length:", vcard.length);

const qrCode = new QRCodeStyling({
    width: 300,
    height: 300,
    data: vcard,
    dotsOptions: { type: "square", color: "#000" },
    backgroundOptions: { color: "#fff" },
});

qrCode.getRawData('png')
    .then(buffer => {
        fs.writeFileSync('test-qr.png', buffer);
        console.log("Success! Saved to test-qr.png");
    })
    .catch(err => {
        console.error("QR Error:", err.message);
    });
