$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $repoRoot 'evidence\2026-08-25\FILE_MANIFEST.csv'

if (-not (Test-Path -LiteralPath $manifestPath)) {
    Write-Error "Manifest not found: $manifestPath"
}

$failed = $false
$rows = Import-Csv -LiteralPath $manifestPath

foreach ($row in $rows) {
    $relativeWindows = $row.RelativePath.Replace('/', '\')
    $path = Join-Path $repoRoot $relativeWindows

    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Write-Host "[FAIL] missing: $($row.RelativePath)"
        $failed = $true
        continue
    }

    $file = Get-Item -LiteralPath $path
    $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToUpperInvariant()
    $expectedHash = $row.SHA256.ToUpperInvariant()
    $sizeOk = $file.Length -eq [int64]$row.Bytes
    $hashOk = $hash -eq $expectedHash

    if ($sizeOk -and $hashOk) {
        Write-Host "[PASS] $($row.RelativePath)"
    }
    else {
        Write-Host "[FAIL] $($row.RelativePath) bytes=$($file.Length)/$($row.Bytes) sha256=$hash/$expectedHash"
        $failed = $true
    }
}

if ($failed) {
    exit 1
}

Write-Host "Verified $($rows.Count) immutable evidence files."
exit 0

