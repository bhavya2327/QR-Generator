<?php

namespace App\Services;

use ZipArchive;
use Illuminate\Support\Str;

class DownloadService
{
    protected QRCodeService $qrCodeService;

    public function __construct(QRCodeService $qrCodeService)
    {
        $this->qrCodeService = $qrCodeService;
    }

    /**
     * Create a ZIP containing QR codes.
     *
     * @param array $urls
     * @param string $format 'png', 'svg', or 'both'
     * @param array $options
     * @return string Path to the temporary ZIP file
     */
    public function createZip(array $urls, string $format = 'both', array $options = []): string
    {
        $zipFile = tempnam(sys_get_temp_dir(), 'qrs_') . '.zip';
        
        $zip = new ZipArchive();
        if ($zip->open($zipFile, ZipArchive::CREATE | ZipArchive::OVERWRITE) !== true) {
            throw new \Exception('Could not create ZIP file.');
        }

        $index = 1;
        foreach ($urls as $url) {
            // Clean filename
            $host = parse_url($url, PHP_URL_HOST) ?? 'url';
            $safeHost = Str::slug($host);
            $baseName = sprintf('qr-%03d-%s', $index, $safeHost);

            if ($format === 'png' || $format === 'both') {
                $pngData = $this->qrCodeService->generatePng($url, 300, $options);
                $path = ($format === 'both') ? "png/{$baseName}.png" : "{$baseName}.png";
                $zip->addFromString($path, $pngData);
            }

            if ($format === 'jpg' || $format === 'both') {
                $jpgData = $this->qrCodeService->generateJpg($url, 300, $options);
                $path = ($format === 'both') ? "jpg/{$baseName}.jpg" : "{$baseName}.jpg";
                $zip->addFromString($path, $jpgData);
            }

            if ($format === 'svg' || $format === 'both') {
                $svgData = $this->qrCodeService->generateSvg($url, 300, $options);
                $path = ($format === 'both') ? "svg/{$baseName}.svg" : "{$baseName}.svg";
                $zip->addFromString($path, $svgData);
            }

            $index++;
        }

        $zip->close();
        return $zipFile;
    }
}
