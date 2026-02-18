
$p = 'c:\InsuranceProject\NotebookLM\saju-app\frontend\index.html'
if (Test-Path $p) {
    Write-Host "Found index.html. Processing..."
    $content = Get-Content $p
    $keep = $content | Select-Object -First 1627
    $tail = @(
        "    </script>",
        "    <script src='qa_loader.js?v=9999'></script>",
        "</body>",
        "</html>"
    )
    $newContent = $keep + $tail
    $newContent | Set-Content $p -Encoding UTF8
    Write-Host "Successfully updated index.html"
} else {
    Write-Error "Could not find index.html at $p"
}
