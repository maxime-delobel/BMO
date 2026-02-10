import socket
import subprocess
import webbrowser
import shutil # New: used to find programs automatically
from app_shortcuts import APP_SHORTCUTS, SPECIAL_CASES

HOST = '192.168.0.1'
PORT = 65432
SPECIAL_CASES = {
    "elden ring": r"C:\Steam\steamapps\common\ELDEN RING\Game\eldenring.exe"
}
def start_pc_bridge():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("BMO Smart Bridge is active...")
        
        while True:
            conn, addr = s.accept()
            data = conn.recv(1024).decode('utf-8')
            print(data)
            match data:
                case str(url) if url.startswith("https://"):
                    webbrowser.open(data)
                case str(app) if app.startswith("APP:"):
                    app_name = data.split(":")[1].lower()
                    app_launcher(app_name)
               
def app_launcher(app_name):
    success = False
    print(f"Trying to open: {app_name}")
     # Method 1: start with "start" option
    if not success:
        try:
            app_name_abbr = app_name
            if APP_SHORTCUTS[app_name]:
                app_name_abbr = APP_SHORTCUTS[app_name]
            print(f"Method 1: Trying with windows start option: start {app_name_abbr}")
            subprocess.Popen(subprocess.Popen(f'start "" {app_name_abbr}', shell=True))
            print(f"Success!")
            success = True
        except Exception as e:
            print(f"Method 4 failed: {e}")
    # Try method 2: Direct command (works for calc, notepad, mspaint, etc.)
    if not success:
        try:
            print(f"Method 2: Trying direct command: {app_name}")
            subprocess.Popen(app_name, shell=True)
            print(f"Success!")
            success = True
        except Exception as e:
            print(f"Method 2 failed: {e}")
    
    # Method 3: Use shutil.which to find in PATH
    path = shutil.which(app_name)
    if not success and path:
        try:
            print(f"Method 3: Found in PATH: {path}")
            subprocess.Popen(path, shell=True)
            print(f"Success!")
            success = True
        except Exception as e:
            print(f"Method 3 failed: {e}")
    
    # Method 4: Try with .exe extension
    if not success:
        try:
            print(f"Method 4: Trying with .exe: {app_name}.exe")
            subprocess.Popen(f"{app_name}.exe", shell=True)
            print(f"Success!")
            success = True
        except Exception as e:
            print(f"Method 4 failed: {e}")
     
    if not success:
        print(f"All methods failed for {app_name}")
    success = False # set again on false so it can be used multiple times in loop



if __name__ == "__main__":
    start_pc_bridge() # Starts the script