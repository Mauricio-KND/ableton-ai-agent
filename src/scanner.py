import time
from typing import Dict, List
from pythonosc import udp_client, osc_server
from pythonosc.dispatcher import Dispatcher
import threading
from config import Config

class AbletonScanner:
    def __init__(self):
        self.state = {
            "tracks": [],
            "tempo": 0.0,
            "master_volume": 0.0
        }
        self.temp_tracks = {}

        self.dispatcher = Dispatcher()
        self.dispatcher.map("/live/song/get/tempo", self._tempo_handler)
        self.dispatcher.map("/live/track/get/name", self._track_name_handler)
        self.dispatcher.map("/live/track/get/volume", self._track_volume_handler)
        self.dispatcher.map("/live/song/get/num_tracks", self._num_tracks_handler)
        self.dispatcher.map("/live/track/get/mute", self._track_mute_handler)

        self.server = osc_server.ThreadingOSCUDPServer((Config.IP, Config.RECEIVE_PORT), self.dispatcher)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        
        # Setup Client
        self.client = udp_client.SimpleUDPClient(Config.IP, Config.SEND_PORT)

    # Callbacks
    def _tempo_handler(self, address, *args):
        self.state["tempo"] = args[0]

    def _num_tracks_handler(self, address, *args):
        num_tracks = args[0]
        print(f"Detectados {num_tracks} tracks. Escaneando nombres...")
        for i in range(num_tracks):
            self.client.send_message("/live/track/get/name", [i])
            self.client.send_message("/live/track/get/volume", [i])
            self.client.send_message("/live/track/get/mute", [i])

    def _track_name_handler(self, address, *args):
        idx, name = args[0], args[1]
        if idx not in self.temp_tracks: self.temp_tracks[idx] = {}
        self.temp_tracks[idx]["name"] = name

    def _track_volume_handler(self, address, *args):
        idx, vol = args[0], args[1]
        if idx not in self.temp_tracks: self.temp_tracks[idx] = {}
        self.temp_tracks[idx]["volume"] = round(vol, 2)

    def _track_mute_handler(self, address, *args):
        idx, mute_state = args[0], args[1]
        if idx not in self.temp_tracks: self.temp_tracks[idx] = {}
        self.temp_tracks[idx]["active"] = not bool(mute_state)

    def scan(self) -> Dict:
        """Ejecuta el escaneo completo de la sesión"""
        print("Iniciando escaneo de sesión...")
        self.temp_tracks = {}
        
        self.client.send_message("/live/song/get/tempo", [])
        self.client.send_message("/live/song/get/num_tracks", [])
        
        time.sleep(1.5)
        
        self.state["tracks"] = [
            {"id": i, **self.temp_tracks[i]} 
            for i in sorted(self.temp_tracks.keys())
        ]
        return self.state

if __name__ == "__main__":
    scanner = AbletonScanner()
    snapshot = scanner.scan()
    print("\n--- SNAPSHOT DE LA SESIÓN ---")
    import json
    print(json.dumps(snapshot, indent=2))
