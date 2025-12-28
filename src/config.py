import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    IP = os.getenv("ABLETON_IP", "127.0.0.1")
    SEND_PORT = int(os.getenv("ABLETON_SEND_PORT", 11000))
    RECEIVE_PORT = int(os.getenv("ABLETON_RECV_PORT", 11001))