<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\CSVService;

class CSVController extends Controller
{
    protected CSVService $csvService;

    public function __construct(CSVService $csvService)
    {
        $this->csvService = $csvService;
    }

    public function upload(Request $request)
    {
        $request->validate([
            'csv_file' => 'required|file|mimes:csv,txt|max:5120', // Max 5MB
        ]);

        try {
            $file = $request->file('csv_file');
            $data = $this->csvService->processFile($file);
            
            return response()->json([
                'success' => true,
                'data' => $data,
                'filename' => $file->getClientOriginalName()
            ]);
        } catch (\Exception $e) {
            \Log::error('CSV Upload Error: ' . $e->getMessage());
            return response()->json([
                'success' => false,
                'message' => 'We couldn\'t process this file. Please check that your CSV contains a valid URL column.'
            ], 422);
        }
    }
}

