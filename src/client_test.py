from pythonosc import udp_client, osc_server
from pythonosc.dispatcher import Dispatcher
import threading
import time

IP = "127.0.0.1"
SEND_PORT = 11000
RECEIVE_PORT = 11001

def print_handler(address, *args):
    print(f"--- [INCOMING] ---")
    print(f"Address: {address} | Data: {args}")

# Setup del Server
dispatcher = Dispatcher()
dispatcher.set_default_handler(print_handler)
server = osc_server.ThreadingOSCUDPServer((IP, RECEIVE_PORT), dispatcher)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()

# 2. Setup del Client
client = udp_client.SimpleUDPClient(IP, SEND_PORT)

def run_test():
    print("Enviando comandos ...")
    
    client.send_message("/live/track/set/volume", [0, 0.7])
    client.send_message("/live/clip/fire", [0, 0])
    client.send_message("/live/song/get/tempo", [])

if __name__ == "__main__":
    run_test()
    time.sleep(1)
