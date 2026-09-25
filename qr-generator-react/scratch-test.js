const { createCanvas } = require('canvas');

const canvas = createCanvas(32, 32);
const ctx = canvas.getContext('2d');
ctx.fillStyle = 'red';
ctx.fillRect(0, 0, 32, 32);
const dataUrl = canvas.toDataURL('image/jpeg', 0.1);
const base64 = dataUrl.split(',')[1];
console.log("Length for 32x32 @ 0.1:", base64.length);

const canvas2 = createCanvas(48, 48);
const ctx2 = canvas2.getContext('2d');
ctx2.fillStyle = 'blue';
ctx2.fillRect(0, 0, 48, 48);
const dataUrl2 = canvas2.toDataURL('image/jpeg', 0.1);
const base642 = dataUrl2.split(',')[1];
console.log("Length for 48x48 @ 0.1:", base642.length);
