<?php

namespace App\Services;

use SimpleSoftwareIO\QrCode\Facades\QrCode;

class QRCodeService
{
    /**
     * Generate an SVG QR code string.
     */
    public function generateSvg(string $data, int $size = 250, array $options = []): string
    {
        return $this->buildQr($data, $size, $options)->generate($data);
    }

    /**
     * Generate a PNG QR code binary string.
     */
    public function generatePng(string $data, int $size = 250, array $options = []): string
    {
        // We use chillerlan/php-qrcode for PNG to avoid the strict 'imagick' requirement of simple-qrcode
        $qrOptions = new \chillerlan\QRCode\QROptions([
            'outputType' => \chillerlan\QRCode\QRCode::OUTPUT_IMAGE_PNG,
            'eccLevel' => \chillerlan\QRCode\QRCode::ECC_L,
            'scale' => ceil($size / 30), // Approximate sizing
            'imageBase64' => false,
        ]);
        
        return (new \chillerlan\QRCode\QRCode($qrOptions))->render($data);
    }

    /**
     * Generate a JPG QR code binary string.
     */
    public function generateJpg(string $data, int $size = 250, array $options = []): string
    {
        $qrOptions = new \chillerlan\QRCode\QROptions([
            'outputType' => \chillerlan\QRCode\QRCode::OUTPUT_IMAGE_JPG,
            'eccLevel' => \chillerlan\QRCode\QRCode::ECC_L,
            'scale' => ceil($size / 30), // Approximate sizing
            'imageBase64' => false,
        ]);
        
        return (new \chillerlan\QRCode\QRCode($qrOptions))->render($data);
    }

    private function buildQr(string $data, int $size, array $options)
    {
        $qr = QrCode::size($size)->margin(1);

        // Colors
        if (!empty($options['color_foreground'])) {
            $qr->color(...$this->hexToRgb($options['color_foreground']));
        }
        if (!empty($options['color_background'])) {
            $qr->backgroundColor(...$this->hexToRgb($options['color_background']));
        }

        // Style (Shape)
        if (!empty($options['qr_style']) && $options['qr_style'] !== 'square') {
            $qr->style($options['qr_style']);
        }

        // Logo
        if (!empty($options['logo_path'])) {
            // merge takes: path, percentage, absolute
            $qr->merge($options['logo_path'], .2, true);
        }

        return $qr;
    }

    private function hexToRgb($hex) {
        $hex = str_replace('#', '', $hex);
        if(strlen($hex) == 3) {
            $r = hexdec(substr($hex,0,1).substr($hex,0,1));
            $g = hexdec(substr($hex,1,1).substr($hex,1,1));
            $b = hexdec(substr($hex,2,1).substr($hex,2,1));
        } else {
            $r = hexdec(substr($hex,0,2));
            $g = hexdec(substr($hex,2,2));
            $b = hexdec(substr($hex,4,2));
        }
        return [$r, $g, $b];
    }
}
