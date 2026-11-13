$ErrorActionPreference = "Stop"

$workspaceRoot = (Resolve-Path "$PSScriptRoot\..").Path
$docxPath = Join-Path $workspaceRoot "AI301_Bao_Cao_Nghiep_Vu_Giai_Phap_Toan_Dien.docx"
$pdfPath = Join-Path $workspaceRoot "AI301_Bao_Cao_Nghiep_Vu_Giai_Phap_Toan_Dien.pdf"
$htmlPath = Join-Path $workspaceRoot "AI301_Executive_Integrated_Dashboard.html"

# Convert DOCX to PDF using Word COM
Write-Host "Converting DOCX to PDF via Word COM..."
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = [Microsoft.Office.Interop.Word.WdAlertLevel]::wdAlertsNone
    $doc = $word.Documents.Open($docxPath)
    # 17 = wdExportFormatPDF
    $doc.ExportAsFixedFormat($pdfPath, 17)
    $doc.Close([Microsoft.Office.Interop.Word.WdSaveOptions]::wdDoNotSaveChanges)
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    Write-Host "PDF created successfully: $pdfPath"
} catch {
    Write-Host "Word COM conversion failed: $_"
    if ($word) {
        $word.Quit()
    }
}

# Distribute files to Downloads
$destinations = @(
    "$env:USERPROFILE\Downloads"
)

$filesToCopy = @($docxPath, $pdfPath, $htmlPath)

foreach ($dest in $destinations) {
    if (Test-Path $dest) {
        foreach ($file in $filesToCopy) {
            if (Test-Path $file) {
                Copy-Item -Path $file -Destination $dest -Force
                Write-Host "Copied $(Split-Path $file -Leaf) -> $dest"
            }
        }
    } else {
        Write-Host "Destination path not found: $dest"
    }
}

Write-Host "All tasks completed!"
