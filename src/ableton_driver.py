from pythonosc import udp_client
from src.config import Config

class AbletonDriver:
    def __init__(self):
        self.client = udp_client.SimpleUDPClient(Config.IP, Config.SEND_PORT)

    def set_track_volume(self, track_index: int, volume: float):
        """Ajusta el volumen de un track específico (0.0 a 1.0)"""
        self.client.send_message("/live/track/set/volume", [track_index, volume])

    def fire_clip(self, track_index: int, clip_index: int):
        self.client.send_message("/live/clip/fire", [track_index, clip_index])

    def get_tempo(self):
        self.client.send_message("/live/song/get/tempo", [])
