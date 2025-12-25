# Open-LLM-VTuber Server Stop Script
# This script stops any running server on port 12393

Write-Host "🔍 Checking for running server on port 12393..." -ForegroundColor Cyan

$connections = Get-NetTCPConnection -LocalPort 12393 -ErrorAction SilentlyContinue

if ($connections) {
    $processIds = $connections | Select-Object -ExpandProperty OwningProcess -Unique
    Write-Host "⚠️  Found $($processIds.Count) process(es) using port 12393" -ForegroundColor Yellow
    
    foreach ($pid in $processIds) {
        try {
            $process = Get-Process -Id $pid -ErrorAction Stop
            Write-Host "🛑 Stopping process $pid ($($process.ProcessName))..." -ForegroundColor Yellow
            Stop-Process -Id $pid -Force -ErrorAction Stop
            Write-Host "✅ Successfully stopped process $pid" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  Could not stop process $pid (may have already stopped)" -ForegroundColor Yellow
        }
    }
    
    Start-Sleep -Seconds 1
    
    # Verify the port is free
    $stillRunning = Get-NetTCPConnection -LocalPort 12393 -ErrorAction SilentlyContinue
    if (-not $stillRunning) {
        Write-Host "✅ Server stopped successfully. Port 12393 is now free." -ForegroundColor Green
    } else {
        Write-Host "⚠️  Warning: Port 12393 may still be in use" -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ No server is currently running on port 12393" -ForegroundColor Green
}
