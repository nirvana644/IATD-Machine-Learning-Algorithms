# ============================================================
# IATD Machine Learning Algorithms - Windows VM provisioning
#
# Run from an ELEVATED PowerShell, from anywhere:
#   powershell -ExecutionPolicy Bypass -File <repo>\provision\provision_windows.ps1
#
# The script runs against the repo copy it lives in - it does NOT
# clone anything. Get the repo onto the machine first (git clone or
# unzip), then run this script from that copy's provision folder.
#
# Every step is checked. The script STOPS at the first failure and
# names the step that failed - if you see "PROVISIONING COMPLETE"
# at the end, everything genuinely worked, including the smoke test.
# Safe to re-run: completed steps are skipped or repeated harmlessly.
#
# NO WORKAROUNDS: a fail is a fail. If the script stops, do not
# rearrange files, rerun from another folder, or install things by
# hand - screenshot the failure output and send it to the SME, and
# the script gets fixed so every future build is right.
# ============================================================
$ErrorActionPreference = "Stop"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Everything is also written to a log file, so a failure can be sent
# back in full even if a screenshot misses the important part.
$log = "$env:TEMP\iatd_provision_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
try { Start-Transcript -Path $log | Out-Null } catch {}
Write-Host "Full log of this run: $log"

$condaDir = "C:\Miniconda3"
$conda    = "$condaDir\Scripts\conda.exe"
$py       = "$condaDir\envs\iatd\python.exe"
$repoRoot = Split-Path -Parent $PSScriptRoot   # script lives in <repo>\provision
$req      = "$repoRoot\requirements.txt"

function Fail([string]$msg) {
    Write-Host ""
    Write-Host "############################################################"
    Write-Host "PROVISIONING FAILED: $msg"
    Write-Host "Send the SME a screenshot of this output AND the log file:"
    Write-Host "  $log"
    Write-Host "The script is safe to re-run once the step is fixed."
    Write-Host "############################################################"
    try { Stop-Transcript | Out-Null } catch {}
    exit 1
}

function Check([string]$label) {
    if ($LASTEXITCODE -ne 0) { Fail "$label (exit code $LASTEXITCODE - see the output above this line)" }
}

# --- 0. Sanity: is this a correct, flattened repo copy? -------
Write-Host "==> Step 0: checking the repo copy this script lives in"
Write-Host "    Repo root: $repoRoot"
$parentName = Split-Path -Leaf (Split-Path -Parent $repoRoot)
$rootName   = Split-Path -Leaf $repoRoot
if ($parentName -eq $rootName) {
    Fail "this checkout is NESTED ('$parentName\$rootName'): the repository still has its content inside an inner folder instead of at the top level. The repository structure must be flattened first - do not work around this by running from a different folder. Screenshot this message and send it to the SME."
}
if (-not (Test-Path $req)) {
    Fail "requirements.txt not found at '$req'. The repo copy this script lives in is incomplete or its structure is wrong. Do not rearrange files to get past this - screenshot this message and send it to the SME."
}
if (-not (Test-Path "$repoRoot\1_a_NumpyRefresher.ipynb")) {
    Fail "lab notebooks not found at '$repoRoot'. The repo structure is wrong - screenshot this message and send it to the SME."
}

# --- 1. Miniconda (Python environment manager) ----------------
Write-Host "==> Step 1: Miniconda"
if (-not (Test-Path $conda)) {
    $installer = "$env:TEMP\miniconda.exe"
    Write-Host "    downloading Miniconda..."
    Invoke-WebRequest "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile $installer
    Write-Host "    installing to $condaDir ..."
    Start-Process $installer -ArgumentList "/S", "/InstallationType=AllUsers", "/AddToPath=1", "/D=$condaDir" -Wait
    if (-not (Test-Path $conda)) { Fail "Miniconda installer finished but '$conda' does not exist" }
} else {
    Write-Host "    already installed - skipping"
}

# Newer conda versions require the Terms of Service to be accepted
# before non-interactive environment creation works. Harmless no-op
# on versions that do not have the 'tos' subcommand.
$eap = $ErrorActionPreference
$ErrorActionPreference = "Continue"
cmd /c "`"$conda`" tos accept >nul 2>&1"
if ($LASTEXITCODE -ne 0) { Write-Host "    (conda tos accept not needed on this conda version - continuing)" }
$ErrorActionPreference = $eap

# --- 2. Python 3.12.7 environment with pinned packages --------
Write-Host "==> Step 2: 'iatd' environment (Python 3.12.7)"
if (-not (Test-Path $py)) {
    & $conda create -y -n iatd python=3.12.7
    Check "conda create of the iatd environment"
    if (-not (Test-Path $py)) { Fail "conda create reported success but '$py' does not exist" }
} else {
    Write-Host "    environment already exists - skipping create"
}

Write-Host "==> Step 3: installing pinned packages into iatd (this is the step that matters)"
& $py -m pip install -r $req
Check "pip install of the pinned packages"

& $py -c "import numpy, pandas, sklearn, matplotlib, seaborn, scipy, joblib, plotly, mlxtend, ipykernel"
Check "import check of the installed packages"
Write-Host "    all course packages import cleanly in iatd"

# --- 3. VS Code + extensions ----------------------------------
Write-Host "==> Step 4: VS Code + Python/Jupyter extensions"
$code = "$env:ProgramFiles\Microsoft VS Code\bin\code.cmd"
if (-not (Test-Path $code)) { $code = "$env:LOCALAPPDATA\Programs\Microsoft VS Code\bin\code.cmd" }
if (-not (Test-Path $code)) {
    winget install -e --id Microsoft.VisualStudioCode --scope machine --accept-package-agreements --accept-source-agreements
    Check "winget install of VS Code"
    $code = "$env:ProgramFiles\Microsoft VS Code\bin\code.cmd"
}
if (-not (Test-Path $code)) { Fail "VS Code is not at '$code' after install" }
& $code --install-extension ms-python.python
Check "install of the VS Code Python extension"
& $code --install-extension ms-toolsai.jupyter
Check "install of the VS Code Jupyter extension"
Write-Host "    VS Code and extensions in place"

# --- 4. Point VS Code at iatd for this repo folder ------------
# Students should never have to pick an interpreter: opening the repo
# folder selects iatd automatically.
Write-Host "==> Step 5: making iatd the default interpreter for the repo folder"
$vsDir = "$repoRoot\.vscode"
if (-not (Test-Path $vsDir)) { New-Item -ItemType Directory -Path $vsDir | Out-Null }
@{ "python.defaultInterpreterPath" = $py } | ConvertTo-Json | Set-Content "$vsDir\settings.json" -Encoding UTF8
Write-Host "    wrote $vsDir\settings.json"

# --- 5. Verify the build (runs every notebook) ----------------
Write-Host "==> Step 6: smoke test - checks versions, then executes all 15 notebooks (several minutes)"
& $py "$PSScriptRoot\smoke_test.py"
Check "smoke test"

Write-Host ""
Write-Host "============================================================"
Write-Host "PROVISIONING COMPLETE - every step passed, including the"
Write-Host "smoke test. Open the repo folder in VS Code: notebooks will"
Write-Host "use the 'iatd' environment automatically."
Write-Host "Log of this run: $log"
Write-Host "============================================================"
try { Stop-Transcript | Out-Null } catch {}
