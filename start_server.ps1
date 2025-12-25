# Open-LLM-VTuber Server Startup Script
# This script automatically stops any existing server and starts a new one

Write-Host "🔍 Checking for existing server on port 12393..." -ForegroundColor Cyan

# Check if port 12393 is in use
$connections = Get-NetTCPConnection -LocalPort 12393 -ErrorAction SilentlyContinue

if ($connections) {
    Write-Host "⚠️  Found existing server running. Stopping it..." -ForegroundColor Yellow
    $processIds = $connections | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($pid in $processIds) {
        try {
            Stop-Process -Id $pid -Force -ErrorAction Stop
            Write-Host "✅ Stopped process $pid" -ForegroundColor Green
        } catch {
            Write-Host "⚠️  Could not stop process $pid (may have already stopped)" -ForegroundColor Yellow
        }
    }
    Start-Sleep -Seconds 2
} else {
    Write-Host "✅ Port 12393 is free" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Starting Open-LLM-VTuber server..." -ForegroundColor Cyan
Write-Host "📍 Server will be available at: http://localhost:12393" -ForegroundColor Green
Write-Host "⏹️  Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
uv run run_server.py
