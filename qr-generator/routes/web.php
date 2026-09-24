<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\QRCodeController;

Route::get('/', function () {
    return view('qr.index');
});

Route::post('/qr/generate', [QRCodeController::class, 'generate'])->name('qr.generate');
Route::get('/qr/{id}/png', [QRCodeController::class, 'downloadPng'])->name('qr.download.png');
Route::get('/qr/{id}/svg', [QRCodeController::class, 'downloadSvg'])->name('qr.download.svg');
Route::post('/qr/bulk-generate', [QRCodeController::class, 'bulkGenerate'])->name('qr.bulk-generate');

Route::post('/csv/upload', [\App\Http\Controllers\CSVController::class, 'upload'])->name('csv.upload');
Route::post('/qr/download-zip', [\App\Http\Controllers\DownloadController::class, 'zip'])->name('qr.download.zip');

Route::get('/sample-csv', function () {
    return response()->download(public_path('example.csv'), 'example.csv', [
        'Content-Type' => 'text/csv',
    ]);
})->name('csv.sample');

