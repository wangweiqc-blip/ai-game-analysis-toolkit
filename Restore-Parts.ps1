param([string]$Directory = $PSScriptRoot)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$restoreRoot = [System.IO.Path]::GetFullPath($Directory)
$manifest = Get-Content -LiteralPath (Join-Path $restoreRoot 'release-manifest.json') -Encoding UTF8 -Raw | ConvertFrom-Json

function Get-LocalPartPath([string]$Name) {
    if ([System.IO.Path]::GetFileName($Name) -ne $Name -or $Name -in @('', '.', '..')) { throw 'Invalid file name in manifest.' }
    return Join-Path $restoreRoot $Name
}

foreach ($part in $manifest.parts) {
    $target = Get-LocalPartPath $part.name
    if (Test-Path -LiteralPath $target) {
        if ((Get-Item -LiteralPath $target).Length -eq $part.bytes -and (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant() -eq $part.sha256) {
            Write-Output ('Verified ' + $part.name)
            continue
        }
        throw ('An existing file has different contents: ' + $target)
    }
    if (-not $part.chunks) { throw ('Missing download: ' + $part.name) }
    $temporary = $target + '.assembling-' + [guid]::NewGuid().ToString('N')
    $outputStream = [System.IO.File]::Open($temporary, [System.IO.FileMode]::CreateNew)
    try {
        foreach ($chunk in $part.chunks) {
            $inputPath = Get-LocalPartPath $chunk.name
            if ((Get-Item -LiteralPath $inputPath).Length -ne $chunk.bytes -or (Get-FileHash -LiteralPath $inputPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $chunk.sha256) {
                throw ('Incomplete or invalid download: ' + $chunk.name)
            }
            $inputStream = [System.IO.File]::OpenRead($inputPath)
            try { $inputStream.CopyTo($outputStream) } finally { $inputStream.Dispose() }
        }
    } finally { $outputStream.Dispose() }
    if ((Get-Item -LiteralPath $temporary).Length -ne $part.bytes -or (Get-FileHash -LiteralPath $temporary -Algorithm SHA256).Hash.ToLowerInvariant() -ne $part.sha256) {
        throw ('Reassembled file failed verification: ' + $temporary)
    }
    [System.IO.File]::Move($temporary, $target)
    Write-Output ('Restored ' + $part.name)
}
Write-Output 'Ready: extract GameAnalysisToolkit-win-x64.7z.001 with 7-Zip.'
