import socket
import subprocess
import webbrowser
import shutil # New: used to find programs automatically

HOST = '192.168.1.3'
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
            
            if data.startswith("APP:"):
                app_name = data.split(":")[1].lower()
                
                # Option A: Check if it's a standard system command (e.g. 'calc')
                path = shutil.which(app_name)
                if path:
                    print(f"BMO found path: {path}")
                    subprocess.Popen(path, shell=True)
                else:
                # Option B: Try to start it as a general shell command
                # This works for apps that have registered themselves with Windows (like 'chrome')
                    try:
                        print(f"BMO attempting to launch: {app_name}")
                        subprocess.Popen(f"start {app_name}", shell=True)
                    except Exception as e:
                        print(f"Failed to launch {app_name}: {e}")
            
            elif data.startswith("http"):
                webbrowser.open(data)

if __name__ == "__main__":
    start_pc_bridge() # Starts the script