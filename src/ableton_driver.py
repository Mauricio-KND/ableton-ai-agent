from pythonosc import udp_client
from .config import Config
import logging

logger = logging.getLogger(__name__)

class AbletonDriver:
    def __init__(self):
        self.client = udp_client.SimpleUDPClient(Config.IP, Config.SEND_PORT)
        logger.info(f"AbletonDriver initialized - sending to {Config.IP}:{Config.SEND_PORT}")

    def set_track_volume(self, track_index: int, volume: float):
        """Adjust the volume of a specific track (0.0 to 1.0)"""
        logger.info(f"Setting track {track_index} volume to {volume}")
        self.client.send_message("/live/track/set/volume", [track_index, volume])

    def fire_clip(self, track_index: int, clip_index: int):
        """Fire/launch a specific clip"""
        logger.info(f"Firing clip {clip_index} on track {track_index}")
        self.client.send_message("/live/clip/fire", [track_index, clip_index])

    def stop_clip(self, track_index: int, clip_index: int):
        """Stop a specific clip"""
        logger.info(f"Stopping clip {clip_index} on track {track_index}")
        self.client.send_message("/live/clip/stop", [track_index, clip_index])

    def get_tempo(self):
        """Request current tempo"""
        logger.info("Requesting current tempo")
        self.client.send_message("/live/song/get/tempo", [])

    def set_tempo(self, tempo: float):
        """Set the master tempo (BPM)"""
        logger.info(f"Setting tempo to {tempo} BPM")
        self.client.send_message("/live/song/set/tempo", [tempo])

    def start_playback(self):
        """Start session playback"""
        logger.info("Starting playback")
        self.client.send_message("/live/song/start_playing", [])

    def stop_playback(self):
        """Stop session playback"""
        logger.info("Stopping playback")
        self.client.send_message("/live/song/stop_playing", [])

    def create_midi_track(self, track_index: int):
        """Create a new MIDI track at specified index"""
        logger.info(f"Creating MIDI track at index {track_index}")
        self.client.send_message("/live/song/create_midi_track", [track_index])

    def create_audio_track(self, track_index: int):
        """Create a new audio track at specified index"""
        logger.info(f"Creating audio track at index {track_index}")
        self.client.send_message("/live/song/create_audio_track", [track_index])

    def delete_track(self, track_index: int):
        """Delete a track"""
        logger.info(f"Deleting track {track_index}")
        self.client.send_message("/live/track/delete", [track_index])

    def set_track_name(self, track_index: int, name: str):
        """Set track name"""
        logger.info(f"Setting track {track_index} name to '{name}'")
        self.client.send_message("/live/track/set/name", [track_index, name])

    def set_track_mute(self, track_index: int, mute: bool):
        """Mute/unmute a track"""
        logger.info(f"Setting track {track_index} mute to {mute}")
        self.client.send_message("/live/track/set/mute", [track_index, int(mute)])

    def add_device(self, track_index: int, device_name: str):
        """Add a device to a track"""
        logger.info(f"Adding device '{device_name}' to track {track_index}")
        self.client.send_message("/live/track/add_device", [track_index, device_name])

    def create_midi_clip(self, track_index: int, length_bars: float = 4.0):
        """Create a MIDI clip on a track"""
        logger.info(f"Creating MIDI clip on track {track_index} with length {length_bars} bars")
        self.client.send_message("/live/clip/create", [track_index, length_bars])

    def set_time_signature(self, numerator: int, denominator: int):
        """Set time signature"""
        logger.info(f"Setting time signature to {numerator}/{denominator}")
        self.client.send_message("/live/song/set/time_signature", [numerator, denominator])

    def set_metronome(self, enabled: bool):
        """Enable/disable metronome"""
        logger.info(f"Setting metronome to {enabled}")
        self.client.send_message("/live/song/set/metronome", [int(enabled)])
