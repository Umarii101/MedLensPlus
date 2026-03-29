$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

Write-Host "Installing/updating mock server dependencies..."
py -m pip install -r .\mock_server_requirements.txt

Write-Host "Starting mock server on 0.0.0.0:8000"
py .\mock_server.py
