# Target Allocation System - Setup Script

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Target Allocation System - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Python found" -ForegroundColor Green

# Check virtual environment
if (-not (Test-Path "venv")) {
    Write-Host ""
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}
else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Verify Streamlit
Write-Host ""
Write-Host "Verifying Streamlit installation..." -ForegroundColor Yellow
streamlit --version
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Streamlit verified" -ForegroundColor Green
} else {
    Write-Host "ERROR: Streamlit installation failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run: .\run_app.ps1" -ForegroundColor White
Write-Host "2. Open your browser" -ForegroundColor White
Write-Host "3. Upload your Excel file with sales data" -ForegroundColor White
Write-Host ""
Write-Host "Sample data file:" -ForegroundColor Cyan
Write-Host "  sales_data_sample.xlsx" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
