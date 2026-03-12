"""
Session management for the Ableton AI Agent

Provides real-time session state tracking and synchronization
with Ableton Live through the MCP interface.
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import threading
import time
import json

from ..utils.logger import get_logger
from ..utils.validators import validate_track_id


@dataclass
class TrackState:
    """Current state of an Ableton track."""
    track_id: int
    name: str
    track_type: str  # 'midi', 'audio', 'return', 'master'
    volume: float = 0.0
    pan: float = 0.0
    mute: bool = False
    solo: bool = False
    armed: bool = False
    is_playing: bool = False
    clip_count: int = 0
    device_count: int = 0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class ClipState:
    """Current state of an Ableton clip."""
    clip_id: int
    track_id: int
    name: str
    length_bars: float
    is_playing: bool = False
    is_triggered: bool = False
    start_time: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class DeviceState:
    """Current state of an Ableton device."""
    device_id: int
    track_id: int
    name: str
    device_type: str  # 'instrument', 'audio_effect', 'midi_effect'
    is_enabled: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class SessionState:
    """Overall Ableton Live session state."""
    tempo: float = 120.0
    time_signature: tuple = (4, 4)
    is_playing: bool = False
    arrangement_overdub: bool = False
    session_automation_record: bool = False
    metronome: bool = False
    current_song_time: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)


class SessionManager:
    """
    Manages real-time session state tracking for Ableton Live.
    
    Provides synchronized state information and change notifications
    to enable intelligent agent decision-making.
    """
    
    def __init__(self, update_interval: float = 1.0):
        """
        Initialize the session manager.
        
        Args:
            update_interval: Interval in seconds for state updates
        """
        self.logger = get_logger(__name__)
        self.update_interval = update_interval
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        
        # State storage
        self.session_state = SessionState()
        self.tracks: Dict[int, TrackState] = {}
        self.clips: Dict[int, ClipState] = {}
        self.devices: Dict[int, DeviceState] = {}
        
        # Change callbacks
        self.state_callbacks: List[Callable[[str, Any], None]] = []
        
        # Thread safety
        self._lock = threading.RLock()
        
    def add_state_callback(self, callback: Callable[[str, Any], None]) -> None:
        """
        Add a callback for state changes.
        
        Args:
            callback: Function to call when state changes
                     (callback_name: str, data: Any) -> None
        """
        with self._lock:
            self.state_callbacks.append(callback)
            
    def remove_state_callback(self, callback: Callable[[str, Any], None]) -> None:
        """
        Remove a state change callback.
        
        Args:
            callback: Callback function to remove
        """
        with self._lock:
            if callback in self.state_callbacks:
                self.state_callbacks.remove(callback)
                
    def _notify_callbacks(self, callback_name: str, data: Any) -> None:
        """Notify all registered callbacks of a state change."""
        for callback in self.state_callbacks:
            try:
                callback(callback_name, data)
            except Exception as e:
                self.logger.error(f"Error in state callback: {e}")
                
    def start_monitoring(self) -> None:
        """Start real-time session monitoring."""
        if self.is_monitoring:
            self.logger.warning("Session monitoring already started")
            return
            
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Started session monitoring")
        
    def stop_monitoring(self) -> None:
        """Stop real-time session monitoring."""
        if not self.is_monitoring:
            return
            
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        self.logger.info("Stopped session monitoring")
        
    def _monitor_loop(self) -> None:
        """Main monitoring loop for state updates."""
        while self.is_monitoring:
            try:
                self.update_session_state()
                time.sleep(self.update_interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.update_interval)
                
    def update_session_state(self) -> None:
        """
        Update the complete session state from Ableton.
        
        This method should be called periodically to keep the state
        synchronized with Ableton Live.
        """
        with self._lock:
            try:
                # This would be implemented with actual MCP calls
                # For now, we'll simulate the structure
                self._fetch_session_info()
                self._fetch_track_info()
                self._fetch_clip_info()
                self._fetch_device_info()
                
            except Exception as e:
                self.logger.error(f"Failed to update session state: {e}")
                
    def _fetch_session_info(self) -> None:
        """Fetch basic session information."""
        # Simulated - would use actual MCP calls
        old_state = self.session_state
        
        # Update session state
        self.session_state.last_updated = datetime.now()
        
        # Check for changes and notify
        if (old_state.tempo != self.session_state.tempo or
            old_state.is_playing != self.session_state.is_playing):
            self._notify_callbacks('session_changed', self.session_state)
            
    def _fetch_track_info(self) -> None:
        """Fetch track information for all tracks."""
        # Simulated - would use actual MCP calls
        # This would iterate through all tracks and update their state
        
        # Example of how track updates would work:
        for track_id in list(self.tracks.keys()):
            old_track = self.tracks[track_id]
            
            # Update track state (simulated)
            self.tracks[track_id].last_updated = datetime.now()
            
            # Check for changes
            if (old_track.volume != self.tracks[track_id].volume or
                old_track.mute != self.tracks[track_id].mute):
                self._notify_callbacks('track_changed', self.tracks[track_id])
                
    def _fetch_clip_info(self) -> None:
        """Fetch clip information for all clips."""
        # Simulated - would use actual MCP calls
        pass
        
    def _fetch_device_info(self) -> None:
        """Fetch device information for all devices."""
        # Simulated - would use actual MCP calls
        pass
        
    def get_session_state(self) -> SessionState:
        """Get current session state."""
        with self._lock:
            return self.session_state
            
    def get_track_state(self, track_id: int) -> Optional[TrackState]:
        """
        Get state for a specific track.
        
        Args:
            track_id: Track ID to retrieve
            
        Returns:
            Track state if found, None otherwise
        """
        track_id = validate_track_id(track_id)
        with self._lock:
            return self.tracks.get(track_id)
            
    def get_clip_state(self, clip_id: int) -> Optional[ClipState]:
        """
        Get state for a specific clip.
        
        Args:
            clip_id: Clip ID to retrieve
            
        Returns:
            Clip state if found, None otherwise
        """
        with self._lock:
            return self.clips.get(clip_id)
            
    def get_device_state(self, device_id: int) -> Optional[DeviceState]:
        """
        Get state for a specific device.
        
        Args:
            device_id: Device ID to retrieve
            
        Returns:
            Device state if found, None otherwise
        """
        with self._lock:
            return self.devices.get(device_id)
            
    def get_tracks_by_type(self, track_type: str) -> List[TrackState]:
        """
        Get all tracks of a specific type.
        
        Args:
            track_type: Track type to filter by
            
        Returns:
            List of track states
        """
        with self._lock:
            return [track for track in self.tracks.values() 
                   if track.track_type == track_type]
                   
    def get_tracks_by_name(self, name: str) -> List[TrackState]:
        """
        Get tracks matching a name (case-insensitive).
        
        Args:
            name: Name to search for
            
        Returns:
            List of matching track states
        """
        name_lower = name.lower()
        with self._lock:
            return [track for track in self.tracks.values() 
                   if name_lower in track.name.lower()]
                   
    def get_playing_clips(self) -> List[ClipState]:
        """Get all currently playing clips."""
        with self._lock:
            return [clip for clip in self.clips.values() if clip.is_playing]
            
    def update_track_state(self, track_id: int, **kwargs) -> None:
        """
        Update track state with new values.
        
        Args:
            track_id: Track ID to update
            **kwargs: State values to update
        """
        track_id = validate_track_id(track_id)
        
        with self._lock:
            if track_id not in self.tracks:
                self.logger.warning(f"Track {track_id} not found for state update")
                return
                
            track = self.tracks[track_id]
            old_state = TrackState(**track.__dict__)
            
            # Update provided fields
            for key, value in kwargs.items():
                if hasattr(track, key):
                    setattr(track, key, value)
                    
            track.last_updated = datetime.now()
            
            # Notify of changes
            self._notify_callbacks('track_updated', {
                'track_id': track_id,
                'old_state': old_state,
                'new_state': track
            })
            
    def update_session_property(self, property_name: str, value: Any) -> None:
        """
        Update a session property.
        
        Args:
            property_name: Property to update
            value: New value
        """
        with self._lock:
            if hasattr(self.session_state, property_name):
                old_value = getattr(self.session_state, property_name)
                setattr(self.session_state, property_name, value)
                self.session_state.last_updated = datetime.now()
                
                # Notify of change
                self._notify_callbacks('session_property_changed', {
                    'property': property_name,
                    'old_value': old_value,
                    'new_value': value
                })
            else:
                self.logger.warning(f"Unknown session property: {property_name}")
                
    def get_state_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current session state.
        
        Returns:
            Dictionary containing state summary
        """
        with self._lock:
            return {
                'session': {
                    'tempo': self.session_state.tempo,
                    'is_playing': self.session_state.is_playing,
                    'time_signature': self.session_state.time_signature
                },
                'tracks': {
                    'total': len(self.tracks),
                    'midi': len([t for t in self.tracks.values() if t.track_type == 'midi']),
                    'audio': len([t for t in self.tracks.values() if t.track_type == 'audio']),
                    'return': len([t for t in self.tracks.values() if t.track_type == 'return']),
                    'playing': len([t for t in self.tracks.values() if t.is_playing])
                },
                'clips': {
                    'total': len(self.clips),
                    'playing': len([c for c in self.clips.values() if c.is_playing])
                },
                'devices': {
                    'total': len(self.devices),
                    'instruments': len([d for d in self.devices.values() if d.device_type == 'instrument']),
                    'effects': len([d for d in self.devices.values() if d.device_type in ['audio_effect', 'midi_effect']])
                }
            }
            
    def export_state(self) -> str:
        """
        Export complete session state as JSON.
        
        Returns:
            JSON string of session state
        """
        with self._lock:
            state = {
                'session': {
                    'tempo': self.session_state.tempo,
                    'time_signature': self.session_state.time_signature,
                    'is_playing': self.session_state.is_playing,
                    'arrangement_overdub': self.session_state.arrangement_overdub,
                    'session_automation_record': self.session_state.session_automation_record,
                    'metronome': self.session_state.metronome,
                    'current_song_time': self.session_state.current_song_time,
                    'last_updated': self.session_state.last_updated.isoformat()
                },
                'tracks': {
                    str(track_id): {
                        'track_id': track.track_id,
                        'name': track.name,
                        'track_type': track.track_type,
                        'volume': track.volume,
                        'pan': track.pan,
                        'mute': track.mute,
                        'solo': track.solo,
                        'armed': track.armed,
                        'is_playing': track.is_playing,
                        'clip_count': track.clip_count,
                        'device_count': track.device_count,
                        'last_updated': track.last_updated.isoformat()
                    }
                    for track_id, track in self.tracks.items()
                },
                'clips': {
                    str(clip_id): {
                        'clip_id': clip.clip_id,
                        'track_id': clip.track_id,
                        'name': clip.name,
                        'length_bars': clip.length_bars,
                        'is_playing': clip.is_playing,
                        'is_triggered': clip.is_triggered,
                        'start_time': clip.start_time,
                        'last_updated': clip.last_updated.isoformat()
                    }
                    for clip_id, clip in self.clips.items()
                },
                'devices': {
                    str(device_id): {
                        'device_id': device.device_id,
                        'track_id': device.track_id,
                        'name': device.name,
                        'device_type': device.device_type,
                        'is_enabled': device.is_enabled,
                        'parameters': device.parameters,
                        'last_updated': device.last_updated.isoformat()
                    }
                    for device_id, device in self.devices.items()
                }
            }
            return json.dumps(state, indent=2)