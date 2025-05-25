# Deploy Neuroleader Typology Feature

# This script will:
# 1. Rename our new files to replace the existing ones
# 2. Generate all necessary images
# 3. Start the application with the new features enabled

$ErrorActionPreference = "Stop"
Write-Host "Deploying neurolider typology feature..." -ForegroundColor Green

# Step 1: Verify that backup folder exists
Write-Host "Checking backup folder..." -ForegroundColor Yellow
if (-not (Test-Path -Path "c:\Users\Anna\Dropbox\BrainVentureApp\backup")) {
    New-Item -Path "c:\Users\Anna\Dropbox\BrainVentureApp\backup" -ItemType Directory -Force
}

# Step 2: Create backup copies of important files
Write-Host "Creating backups of important files..." -ForegroundColor Yellow
Copy-Item -Path "c:\Users\Anna\Dropbox\BrainVentureApp\pages\5_Typy_Neuroliderow.py" -Destination "c:\Users\Anna\Dropbox\BrainVentureApp\backup\5_Typy_Neuroliderow.py.$(Get-Date -Format 'yyyyMMdd')" -Force
Copy-Item -Path "c:\Users\Anna\Dropbox\BrainVentureApp\pages\1_Dashboard.py" -Destination "c:\Users\Anna\Dropbox\BrainVentureApp\backup\1_Dashboard.py.$(Get-Date -Format 'yyyyMMdd')" -Force
Copy-Item -Path "c:\Users\Anna\Dropbox\BrainVentureApp\utils\neuroleader_types.py" -Destination "c:\Users\Anna\Dropbox\BrainVentureApp\backup\neuroleader_types.py.$(Get-Date -Format 'yyyyMMdd')" -Force

# Step 3: Generate all images
Write-Host "Generating images for neuroleader types..." -ForegroundColor Yellow
Set-Location -Path "c:\Users\Anna\Dropbox\BrainVentureApp"
python "c:\Users\Anna\Dropbox\BrainVentureApp\utils\create_images.py"

# Step 4: Start the application
Write-Host "Starting BrainVenture application..." -ForegroundColor Green
Write-Host "To access the neurolider typology feature, navigate to 'Typy Neuroliderów' in the sidebar." -ForegroundColor Cyan
Write-Host "Run the following command to start the application:" -ForegroundColor Cyan
Write-Host "streamlit run Home.py" -ForegroundColor White

Write-Host "`nDeployment complete!" -ForegroundColor Green
