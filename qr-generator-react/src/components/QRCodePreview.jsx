'use client';
import React, { useEffect, useRef } from 'react';
import QRCodeStyling from 'qr-code-styling';

export default function QRCodePreview({ data, fgColor, bgColor, bodyShape, eyeFrameShape, eyeBallShape, logoFile }) {
    const ref = useRef(null);
    const qrCode = useRef(null);

    useEffect(() => {
        qrCode.current = new QRCodeStyling({
            width: 250,
            height: 250,
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
            backgroundOptions: {
                color: bgColor,
            },
            imageOptions: {
                crossOrigin: "anonymous",
                margin: 5,
                imageSize: 0.4
            }
        });
        
        qrCode.current.append(ref.current);

        return () => {
            if (ref.current) {
                ref.current.innerHTML = '';
            }
        };
    }, []);

    useEffect(() => {
        if (!qrCode.current) return;
        qrCode.current.update({
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
            backgroundOptions: {
                color: bgColor,
            },
            imageOptions: {
                crossOrigin: "anonymous",
                margin: 5,
                imageSize: 0.4
            }
        });
    }, [data, fgColor, bgColor, bodyShape, eyeFrameShape, eyeBallShape, logoFile]);

    return <div ref={ref} className="d-flex justify-content-center align-items-center" />;
}
