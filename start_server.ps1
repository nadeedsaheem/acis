# start_server.ps1
# Kills any process on port 8000, then starts the ACIS GraphRAG API server.

Write-Host "Checking for processes on port 8000..."

$netstatOutput = netstat -ano | findstr ":8000 "
if ($netstatOutput) {
    $pid = ($netstatOutput -split '\s+')[-1]
    Write-Host "Found process PID $pid on port 8000. Terminating..."
    taskkill /PID $pid /F | Out-Null
    Start-Sleep -Seconds 1
    Write-Host "Port 8000 freed."
} else {
    Write-Host "Port 8000 is free."
}

$env:PYTHONPATH = "src"
Write-Host "Starting ACIS GraphRAG API server..."
python src/api_server.py
