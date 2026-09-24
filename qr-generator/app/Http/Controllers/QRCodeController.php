<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\QRCodeService;
use Illuminate\Support\Str;

class QRCodeController extends Controller
{
    protected QRCodeService $qrCodeService;

    public function __construct(QRCodeService $qrCodeService)
    {
        $this->qrCodeService = $qrCodeService;
    }

    public function generate(Request $request)
    {
        $data = $this->buildDataString($request);
        $options = $this->extractOptions($request);

        $svg = $this->qrCodeService->generateSvg($data, 300, $options);
        
        // Encode state into ID so we can regenerate it on download
        $payload = ['data' => $data, 'options' => $options];
        $id = base64_encode(json_encode($payload));

        return response()->json([
            'success' => true,
            'svg' => $svg,
            'id' => $id,
            'url' => substr($data, 0, 50) . (strlen($data) > 50 ? '...' : '')
        ]);
    }

    public function downloadPng($id)
    {
        $payload = json_decode(base64_decode($id), true);
        if (!$payload || !isset($payload['data'])) abort(400, 'Invalid QR Data');

        $png = $this->qrCodeService->generatePng($payload['data'], 300, $payload['options'] ?? []);
        $filename = 'qr-code-' . time() . '.png';

        return response($png)
            ->header('Content-Type', 'image/png')
            ->header('Content-Disposition', 'attachment; filename="' . $filename . '"');
    }

    public function downloadSvg($id)
    {
        $payload = json_decode(base64_decode($id), true);
        if (!$payload || !isset($payload['data'])) abort(400, 'Invalid QR Data');

        $svg = $this->qrCodeService->generateSvg($payload['data'], 300, $payload['options'] ?? []);
        $filename = 'qr-code-' . time() . '.svg';

        return response($svg)
            ->header('Content-Type', 'image/svg+xml')
            ->header('Content-Disposition', 'attachment; filename="' . $filename . '"');
    }

    public function bulkGenerate(Request $request)
    {
        $urls = $request->input('urls');
        $options = $request->input('options', []);
        $results = [];

        foreach ($urls as $url) {
            $svg = $this->qrCodeService->generateSvg($url, 300, $options);
            $payload = ['data' => $url, 'options' => $options];
            $id = base64_encode(json_encode($payload));
            $results[] = [
                'url' => $url,
                'svg' => $svg,
                'id' => $id
            ];
        }

        return response()->json([
            'success' => true,
            'data' => $results
        ]);
    }

    private function buildDataString(Request $request): string
    {
        $type = $request->input('type', 'url');
        
        switch ($type) {
            case 'text':
                return $request->input('text', '');
            case 'email':
                $to = $request->input('email', '');
                $subject = rawurlencode($request->input('email_subject', ''));
                $body = rawurlencode($request->input('email_body', ''));
                return "mailto:$to?subject=$subject&body=$body";
            case 'phone':
                return "tel:" . $request->input('phone', '');
            case 'sms':
                $phone = $request->input('sms_phone', '');
                $msg = $request->input('sms_message', '');
                return "smsto:$phone:$msg";
            case 'vcard':
                $fn = $request->input('vcard_first_name', '');
                $ln = $request->input('vcard_last_name', '');
                $tel = $request->input('vcard_phone', '');
                $email = $request->input('vcard_email', '');
                $org = $request->input('vcard_company', '');
                
                return "BEGIN:VCARD\nVERSION:3.0\nN:$ln;$fn;;;\nFN:$fn $ln\nORG:$org\nTEL:$tel\nEMAIL:$email\nEND:VCARD";
            case 'wifi':
                $ssid = $request->input('wifi_ssid', '');
                $pass = $request->input('wifi_password', '');
                $enc = $request->input('wifi_encryption', 'WPA');
                return "WIFI:T:$enc;S:$ssid;P:$pass;;";
            case 'url':
            default:
                return $request->input('url', '');
        }
    }

    private function extractOptions(Request $request): array
    {
        $options = [
            'color_foreground' => $request->input('color_foreground', '#000000'),
            'color_background' => $request->input('color_background', '#ffffff'),
            'qr_style' => $request->input('qr_style', 'square')
        ];

        if ($request->hasFile('logo_file')) {
            // Save logo temporarily for generation
            $path = $request->file('logo_file')->store('temp_logos');
            $options['logo_path'] = storage_path('app/' . $path);
        }

        return $options;
    }
}
