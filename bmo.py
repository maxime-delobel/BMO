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

def wake_pc(url: str):
    """
    Turns on the pc via wake-on-lan.
    Use this when the user asks to turn on the computer or something similar
    """
    print(f"--- BMO Sending Command: {url} ---")
    try:
        send_magic_packet('D8-43-AE-66-85-90')
        return f"Successfully opened send the magic packet to wake up pc"
    except Exception as e:
        return f"Error: Couldn't turn on pc: ({e})"

# 3. INITIALIZE CLIENT
client = genai.Client()

# 4. START CHAT WITH AUTOMATIC TOOLS
# We enable 'automatic_function_calling' so BMO actually sends the signal 
# without you having to manually handle the request.
chat = client.chats.create(
    model="gemini-3-flash-preview",
    config={
        'tools': [open_pc_site, wake_pc, google_search],
        'automatic_function_calling': {'disable': False},
        'system_instruction': (
            "Je bent BMO. Geef ALTIJD een kort tekstueel antwoord aan de gebruiker, "
            "ook als je een tool aanroept of een zoekopdracht uitvoert. "
            "Houd je antwoorden beknopt (max 300 tekens)."
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