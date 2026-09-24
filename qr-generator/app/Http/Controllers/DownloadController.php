<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\DownloadService;

class DownloadController extends Controller
{
    protected DownloadService $downloadService;

    public function __construct(DownloadService $downloadService)
    {
        $this->downloadService = $downloadService;
    }

    public function zip(Request $request)
    {
        $request->validate([
            'urls' => 'required|array',
            'urls.*' => 'required|url',
            'format' => 'required|in:png,svg,jpg,both'
        ]);

        try {
            $urls = $request->input('urls');
            $format = $request->input('format');
            $options = $request->input('options', []);
            
            $zipPath = $this->downloadService->createZip($urls, $format, $options);
            $filename = 'qr-codes-' . date('Y-m-d-His') . '.zip';

            return response()->download($zipPath, $filename)->deleteFileAfterSend(true);
        } catch (\Exception $e) {
            \Log::error('ZIP Generation Error: ' . $e->getMessage());
            return response()->json(['success' => false, 'message' => 'Failed to generate ZIP.'], 500);
        }
    }
}

