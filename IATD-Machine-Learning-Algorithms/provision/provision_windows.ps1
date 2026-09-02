# ============================================================
# IATD Machine Learning Algorithms - Windows VM provisioning
# Run in an elevated PowerShell. Builds the exact environment
# every lab in this repository is verified against.
# ============================================================
$ErrorActionPreference = "Stop"

# --- 1. Miniconda (Python environment manager) ---------------
$condaDir = "C:\Miniconda3"
if (-not (Test-Path $condaDir)) {
    $installer = "$env:TEMP\miniconda.exe"
    Invoke-WebRequest "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile $installer
    Start-Process $installer -ArgumentList "/S", "/InstallationType=AllUsers", "/AddToPath=1", "/D=$condaDir" -Wait
}
$conda = "$condaDir\Scripts\conda.exe"

# --- 2. Python 3.12.7 environment with pinned packages -------
& $conda create -y -n iatd python=3.12.7
& "$condaDir\envs\iatd\python.exe" -m pip install -r "$PSScriptRoot\..\requirements.txt"

# --- 3. VS Code + extensions ---------------------------------
winget install -e --id Microsoft.VisualStudioCode --scope machine --accept-package-agreements --accept-source-agreements
$code = "$env:ProgramFiles\Microsoft VS Code\bin\code.cmd"
& $code --install-extension ms-python.python
& $code --install-extension ms-toolsai.jupyter

# --- 4. Course repository ------------------------------------
# (skip if this script is already running from a cloned copy)
$repo = "C:\IATD\IATD-Machine-Learning-Algorithms"
if (-not (Test-Path $repo)) {
    winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements
    & "$env:ProgramFiles\Git\cmd\git.exe" clone https://github.com/Institute-of-Applied-Technology/IATD-Machine-Learning-Algorithms.git $repo
}

# --- 5. Verify the build -------------------------------------
& "$condaDir\envs\iatd\python.exe" "$repo\provision\smoke_test.py"
Write-Host "Provisioning complete. Open the repo folder in VS Code and select the 'iatd' environment as the kernel."
