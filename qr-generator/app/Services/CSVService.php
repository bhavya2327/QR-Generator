<?php

namespace App\Services;

use League\Csv\Reader;
use Illuminate\Http\UploadedFile;

class CSVService
{
    /**
     * Process an uploaded CSV file and extract URLs.
     *
     * @param UploadedFile $file
     * @return array
     */
    public function processFile(UploadedFile $file): array
    {
        $csv = Reader::createFromPath($file->getRealPath(), 'r');
        $csv->setHeaderOffset(0); // Assume first row is header initially

        $headers = $csv->getHeader();
        
        $urlColumn = $this->detectUrlColumn($headers);
        
        $records = [];
        if ($urlColumn !== null) {
            // We have a header with a URL column
            foreach ($csv->getRecords() as $index => $record) {
                $records[] = $this->parseRow($record[$urlColumn], $index);
            }
        } else {
            // Check if there are no headers and it's just a single column CSV
            $csv->setHeaderOffset(null); // Remove header offset
            foreach ($csv->getRecords() as $index => $record) {
                // Check every column for a valid URL
                $foundUrl = null;
                foreach ($record as $cell) {
                    if (filter_var(trim($cell), FILTER_VALIDATE_URL)) {
                        $foundUrl = trim($cell);
                        break;
                    }
                }
                
                // If not found, just use the first column to show the error
                $value = $foundUrl ?? (isset($record[0]) ? trim($record[0]) : '');
                $records[] = $this->parseRow($value, $index + 1);
            }
        }

        $validCount = 0;
        $invalidCount = 0;
        foreach ($records as $record) {
            if ($record['status'] === 'Valid') {
                $validCount++;
            } else {
                $invalidCount++;
            }
        }

        return [
            'total' => count($records),
            'valid' => $validCount,
            'invalid' => $invalidCount,
            'records' => $records,
            'headers_detected' => !empty($headers),
            'url_column' => $urlColumn
        ];
    }

    private function detectUrlColumn(array $headers): ?string
    {
        $possibleColumns = ['url', 'link', 'website', 'website_url', 'vcard'];
        
        foreach ($headers as $header) {
            if (in_array(strtolower(trim($header)), $possibleColumns)) {
                return $header;
            }
        }
        
        return null;
    }

    private function parseRow(string $value, int $index): array
    {
        $value = trim($value);
        $isValid = filter_var($value, FILTER_VALIDATE_URL) !== false;
        
        return [
            'index' => $index,
            'url' => $value,
            'status' => $isValid ? 'Valid' : 'Invalid',
        ];
    }
}
