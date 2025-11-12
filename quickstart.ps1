# Quick Start Script for Statistician Package Development (Windows)
# PowerShell version

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Statistician - Quick Start Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow

$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "Error: Python is not installed!" -ForegroundColor Red
    exit 1
}

$pythonVersion = & $pythonCmd --version 2>&1
Write-Host "Found $pythonVersion" -ForegroundColor Green

# Check if Python version is >= 3.8
$versionOutput = & $pythonCmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
$major, $minor = $versionOutput.Split('.')

if ([int]$major -lt 3 -or ([int]$major -eq 3 -and [int]$minor -lt 8)) {
    Write-Host "Error: Python 3.8 or higher is required!" -ForegroundColor Red
    Write-Host "Current version: $pythonVersion" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Python version OK" -ForegroundColor Green
Write-Host ""

# Create virtual environment if it doesn't exist
if (-Not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    & $pythonCmd -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
& python -m pip install --upgrade pip --quiet
Write-Host "✓ pip upgraded" -ForegroundColor Green
Write-Host ""

# Install package in editable mode with dev dependencies
Write-Host "Installing package with development dependencies..." -ForegroundColor Yellow
& pip install -e ".[dev]" --quiet
Write-Host "✓ Package installed in editable mode" -ForegroundColor Green
Write-Host ""

# Run tests
Write-Host "Running tests..." -ForegroundColor Yellow
Write-Host "==========================================" -ForegroundColor Cyan
& pytest tests/ -v
$testExitCode = $LASTEXITCODE
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

if ($testExitCode -eq 0) {
    Write-Host "✓ All tests passed!" -ForegroundColor Green
} else {
    Write-Host "✗ Some tests failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please fix the failing tests before publishing." -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Check code formatting
Write-Host "Checking code formatting..." -ForegroundColor Yellow
$blackOutput = & black --check statistician/ tests/ 2>&1 | Select-Object -First 10
$blackExitCode = $LASTEXITCODE

if ($blackExitCode -eq 0) {
    Write-Host "✓ Code formatting OK" -ForegroundColor Green
} else {
    Write-Host "⚠ Code formatting issues found" -ForegroundColor Yellow
    Write-Host "Run: black statistician/ tests/" -ForegroundColor Yellow
}
Write-Host ""

# Check import sorting
Write-Host "Checking import sorting..." -ForegroundColor Yellow
$isortOutput = & isort --check-only statistician/ tests/ 2>&1 | Select-Object -First 10
$isortExitCode = $LASTEXITCODE

if ($isortExitCode -eq 0) {
    Write-Host "✓ Import sorting OK" -ForegroundColor Green
} else {
    Write-Host "⚠ Import sorting issues found" -ForegroundColor Yellow
    Write-Host "Run: isort statistician/ tests/" -ForegroundColor Yellow
}
Write-Host ""

# Run linting
Write-Host "Running flake8 linting..." -ForegroundColor Yellow
& flake8 statistician/ tests/ --count --statistics
$flake8ExitCode = $LASTEXITCODE

if ($flake8ExitCode -eq 0) {
    Write-Host "✓ No linting issues" -ForegroundColor Green
} else {
    Write-Host "⚠ Linting issues found" -ForegroundColor Yellow
}
Write-Host ""

# Display package info
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Package Information" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
& python -c "import statistician; print(f'Package: statistician'); print(f'Version: {statistician.__version__}'); print(f'Location: {statistician.__file__}')"
Write-Host ""

# Test basic functionality
Write-Host "Testing basic functionality..." -ForegroundColor Yellow
& python -c "from statistician import mean, median; print(f'mean([1,2,3,4,5]) = {mean([1,2,3,4,5])}'); print(f'median([1,2,3,4,5]) = {median([1,2,3,4,5])}')"
Write-Host "✓ Basic functions working" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Activate the virtual environment:" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Run the example script:" -ForegroundColor White
Write-Host "   python example.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Make changes and test:" -ForegroundColor White
Write-Host "   pytest tests/" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Before committing, format your code:" -ForegroundColor White
Write-Host "   black statistician/ tests/" -ForegroundColor Gray
Write-Host "   isort statistician/ tests/" -ForegroundColor Gray
Write-Host ""
Write-Host "5. When ready to publish, see PUBLISHING.md" -ForegroundColor White
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan