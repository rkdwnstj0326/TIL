$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$taskModules = @(
    'src.collection.download_stats',
    'src.collection.collect_cases',
    'src.preprocessing.extract_sources',
    'src.preprocessing.parse_cases',
    'src.preprocessing.clean_stats'
)
foreach ($taskModule in $taskModules) {
    & '.\.venv\Scripts\python.exe' -m $taskModule
    if ($LASTEXITCODE -ne 0) { throw "Stopped: $taskModule" }
}
& '.\.venv\Scripts\python.exe' -c 'from src.collection.collect_cases import collect; collect((5,8,12))'
if ($LASTEXITCODE -ne 0) { throw 'Additional insurance cases collection failed.' }
& '.\.venv\Scripts\python.exe' -m src.preprocessing.parse_cases
if ($LASTEXITCODE -ne 0) { throw 'Case extraction failed.' }
& '.\.venv\Scripts\python.exe' -m src.analysis.phase0_audit
if ($LASTEXITCODE -ne 0) { throw 'Data audit failed.' }
& '.\.venv\Scripts\python.exe' -m src.collection.expand_insurers
if ($LASTEXITCODE -ne 0) { throw 'Insurer expansion validation failed.' }
& '.\.venv\Scripts\python.exe' -m src.collection.collect_history
if ($LASTEXITCODE -ne 0) { throw 'Historical quarter collection/validation failed.' }
