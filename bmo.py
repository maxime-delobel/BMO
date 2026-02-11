from google import genai
import socket
from wakeonlan import send_magic_packet

# 1. SETUP CONSTANTS
PC_IP = "192.168.0.1"  # <--- CHANGE THIS to your actual PC IP
PORT = 65432


# 2. DEFINE THE TOOL (Must be defined BEFORE the chat)
def open_pc_site(url: str):
    """
    Opens a specific website on the user's computer. 
    Use this when the user asks to 'open' a site,  or 'go to' a URL.
    """
    print(f"--- BMO Sending Command: {url} ---")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5) # Don't wait forever if PC is off
            s.connect((PC_IP, PORT))
            s.sendall(url.encode('utf-8'))
        return f"Successfully opened {url} on your PC!"
    except Exception as e:
        return f"Error: I couldn't connect to your PC. Is the bridge running? ({e})"
def google_search(zoekterm: str):
    """
    zoekt en toont informatie in de browser wanneer de gebruiker een vraag stelt.
    Use this when the user asks to search for something. Or when user asks a question where he/she needs extra information about a topic. Also use this function when the user ask something (should be used next to the normal response)
    """
    url = f"https://google.com/search?q={zoekterm}"
    print(f"--- BMO Sending Command: {url} ---")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5) # Don't wait forever if PC is off
            s.connect((PC_IP, PORT))
            s.sendall(url.encode('utf-8'))
        return f"Successfully performed the search on google for {url}"
    except Exception as e:
        return f"Error: I couldn't connect to your PC. Is the bridge running? ({e})"

def open_app(nativeAppName: str):
    """
    Opent een applicatie op windows
    Use this when the user asks to open an app 
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5) # Don't wait forever if PC is off
            s.connect((PC_IP, PORT))
            nativeAppName = "APP:" + nativeAppName #zodat de listener kan filteren
            s.sendall(nativeAppName.encode('utf-8'))
        return f"Successfully opened app: {nativeAppName}"
    except Exception as e:
        return f"Error: I couldn't connect to your PC. Is the bridge running? ({e})"

def open_game():
    """
    Opent een game op de computer
    Use this when the users states he/she wants to play a specific game or something similar.
    """

def open_steam():
    """
    Opent steam op de computer
    Use this when the users states he/she wants to play a game or something similar.
    """

def copy_to_clipboard(text):
    """
    Zet de text die wordt meegegeven in de functie (werd ingesproken door de gebruiker) in het clipboard van de computer
    Use this when the user asks to save certain text to clipboard
    """

def type_text(text):
    """
    Typt de text die wordt meegegeven in de functie op de PC
    Use this when the user asks to type something
    """
def take_screenshot():
    """
    Neemt een schermafbeelding van het scherm dat op de pc wordt getoond
    Use this when the user asks to take a screenshot or something similar.
    """
def adjust_volume(percentage):
    """
    Verandert het volumeniveau naar het meegegeven percentage op de PC
    Use this when the user asks to alter the volume level to a given percentage
    """
def mute_unmute():
    """
    Mute of unmute het volume op de PC
    Use this when the user asks to mute or unmute
    """
def wake_pc(url: str):
    """
    Turns on the pc via wake-on-lan.
    Use this when the user asks to turn on the computer or something similar
    """
    print(f"--- BMO Sending Command: {url} ---")
    try:
        send_magic_packet('D8-43-AE-66-85-90')
        return f"Successfully send the magic packet to wake up pc"
    except Exception as e:
        return f"Error: Couldn't turn on pc: ({e})"

# 3. INITIALIZE CLIENT
client = genai.Client()

# 4. START CHAT WITH AUTOMATIC TOOLS
# We enable 'automatic_function_calling' so BMO actually sends the signal 
# without you having to manually handle the request.
chat = client.chats.create(
    model="gemini-2.5-flash",
    config= {
        'tools': [open_pc_site, wake_pc, google_search, open_app, open_game, open_steam, copy_to_clipboard,type_text, take_screenshot, adjust_volume, mute_unmute],
        'automatic_function_calling': {'disable': False},
        'system_instruction': (
            "Je bent BMO. Geef ALTIJD een kort tekstueel antwoord aan de gebruiker, "
            "ook als je een tool aanroept of een zoekopdracht uitvoert. "
            "Houd je antwoorden beknopt (max 300 tekens). Als er een app moet worden geopend, ga ervan uit dat windows in het engels staat ingesteld"
        )
    }
)

print("BMO is online!")

# 5. THE MAIN LOOP
while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            break
            
        # This sends your message to Gemini. 
        # If Gemini decides to call open_pc_site, it happens automatically here.
        response = chat.send_message(user_input)
        
        print(f"BMO: {response.text}")
        
    except Exception as e:
        print(f"BMO Glitch: {e}")