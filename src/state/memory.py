"""
Memory management for the Ableton AI Agent

Provides short-term memory capabilities to track created elements
and maintain context for sequential commands.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json


@dataclass
class TrackMemory:
    """Memory entry for a created track."""
    track_id: int
    name: str
    track_type: str  # 'midi' or 'audio'
    created_at: datetime
    devices: List[str] = field(default_factory=list)
    clips: List[int] = field(default_factory=list)
    last_used: Optional[datetime] = None


@dataclass
class ClipMemory:
    """Memory entry for a created clip."""
    clip_id: int
    track_id: int
    name: str
    length_bars: int
    created_at: datetime
    last_used: Optional[datetime] = None


@dataclass
class DeviceMemory:
    """Memory entry for an added device."""
    device_id: int
    track_id: int
    name: str
    device_type: str  # 'instrument' or 'effect'
    created_at: datetime
    parameters: Dict[str, Any] = field(default_factory=dict)


class MemoryManager:
    """
    Manages short-term memory for the Ableton AI Agent.
    
    Tracks created tracks, clips, and devices to provide context
    for subsequent commands and enable references like "the bass track".
    """
    
    def __init__(self, max_age_hours: int = 2):
        """
        Initialize the memory manager.
        
        Args:
            max_age_hours: Maximum age for memory entries before cleanup
        """
        self.max_age = timedelta(hours=max_age_hours)
        self.tracks: Dict[int, TrackMemory] = {}
        self.clips: Dict[int, ClipMemory] = {}
        self.devices: Dict[int, DeviceMemory] = {}
        self.name_to_track_id: Dict[str, int] = {}
        self.last_cleanup = datetime.now()
        
    def add_track(self, track_id: int, name: str, track_type: str = 'midi') -> None:
        """
        Add a track to memory.
        
        Args:
            track_id: Ableton track ID
            name: Track name
            track_type: Track type ('midi' or 'audio')
        """
        self.tracks[track_id] = TrackMemory(
            track_id=track_id,
            name=name,
            track_type=track_type,
            created_at=datetime.now()
        )
        self.name_to_track_id[name.lower()] = track_id
        
    def add_clip(self, clip_id: int, track_id: int, name: str, length_bars: int) -> None:
        """
        Add a clip to memory.
        
        Args:
            clip_id: Clip ID
            track_id: Parent track ID
            name: Clip name
            length_bars: Length in bars
        """
        self.clips[clip_id] = ClipMemory(
            clip_id=clip_id,
            track_id=track_id,
            name=name,
            length_bars=length_bars,
            created_at=datetime.now()
        )
        
        # Update track's clip list
        if track_id in self.tracks:
            self.tracks[track_id].clips.append(clip_id)
            
    def add_device(self, device_id: int, track_id: int, name: str, device_type: str) -> None:
        """
        Add a device to memory.
        
        Args:
            device_id: Device ID
            track_id: Parent track ID
            name: Device name
            device_type: Device type ('instrument' or 'effect')
        """
        self.devices[device_id] = DeviceMemory(
            device_id=device_id,
            track_id=track_id,
            name=name,
            device_type=device_type,
            created_at=datetime.now()
        )
        
        # Update track's device list
        if track_id in self.tracks:
            self.tracks[track_id].devices.append(name)
            
    def get_track_by_name(self, name: str) -> Optional[int]:
        """
        Find track ID by name (case-insensitive).
        
        Args:
            name: Track name to search for
            
        Returns:
            Track ID if found, None otherwise
        """
        return self.name_to_track_id.get(name.lower())
        
    def get_track_by_type(self, track_type: str) -> Optional[int]:
        """
        Find a track by type.
        
        Args:
            track_type: Track type ('midi' or 'audio')
            
        Returns:
            Track ID if found, None otherwise
        """
        for track_id, track_mem in self.tracks.items():
            if track_mem.track_type == track_type:
                return track_id
        return None
        
    def find_track_with_device(self, device_name: str) -> Optional[int]:
        """
        Find track that contains a specific device.
        
        Args:
            device_name: Device name to search for
            
        Returns:
            Track ID if found, None otherwise
        """
        for track_id, track_mem in self.tracks.items():
            if device_name.lower() in [d.lower() for d in track_mem.devices]:
                return track_id
        return None
        
    def get_recent_track(self, track_type: Optional[str] = None) -> Optional[int]:
        """
        Get the most recently used track.
        
        Args:
            track_type: Optional track type filter
            
        Returns:
            Track ID if found, None otherwise
        """
        candidates = []
        for track_id, track_mem in self.tracks.items():
            if track_type is None or track_mem.track_type == track_type:
                candidates.append((track_mem.last_used or track_mem.created_at, track_id))
        
        if candidates:
            return max(candidates, key=lambda x: x[0])[1]
        return None
        
    def update_track_usage(self, track_id: int) -> None:
        """
        Update the last used time for a track.
        
        Args:
            track_id: Track ID to update
        """
        if track_id in self.tracks:
            self.tracks[track_id].last_used = datetime.now()
            
    def cleanup_old_entries(self) -> None:
        """Remove old entries to prevent memory bloat."""
        now = datetime.now()
        
        # Clean up old tracks
        old_tracks = [
            track_id for track_id, track_mem in self.tracks.items()
            if now - track_mem.created_at > self.max_age
        ]
        for track_id in old_tracks:
            self.remove_track(track_id)
            
        self.last_cleanup = now
        
    def remove_track(self, track_id: int) -> None:
        """
        Remove a track and all associated memory.
        
        Args:
            track_id: Track ID to remove
        """
        if track_id in self.tracks:
            track_mem = self.tracks[track_id]
            
            # Remove from name mapping
            if track_mem.name.lower() in self.name_to_track_id:
                del self.name_to_track_id[track_mem.name.lower()]
            
            # Remove associated clips
            for clip_id in track_mem.clips:
                if clip_id in self.clips:
                    del self.clips[clip_id]
            
            # Remove associated devices
            for device_id, device_mem in list(self.devices.items()):
                if device_mem.track_id == track_id:
                    del self.devices[device_id]
            
            # Remove track
            del self.tracks[track_id]
            
    def get_context_summary(self) -> Dict[str, Any]:
        """
        Get a summary of current memory state for LLM context.
        
        Returns:
            Dictionary containing memory summary
        """
        self.cleanup_old_entries()
        
        return {
            'tracks': {
                track_id: {
                    'name': track_mem.name,
                    'type': track_mem.track_type,
                    'devices': track_mem.devices,
                    'clip_count': len(track_mem.clips)
                }
                for track_id, track_mem in self.tracks.items()
            },
            'total_tracks': len(self.tracks),
            'total_clips': len(self.clips),
            'total_devices': len(self.devices)
        }
        
    def export_state(self) -> str:
        """
        Export memory state as JSON for persistence.
        
        Returns:
            JSON string of memory state
        """
        state = {
            'tracks': {
                str(track_id): {
                    'track_id': track_mem.track_id,
                    'name': track_mem.name,
                    'track_type': track_mem.track_type,
                    'created_at': track_mem.created_at.isoformat(),
                    'devices': track_mem.devices,
                    'clips': track_mem.clips,
                    'last_used': track_mem.last_used.isoformat() if track_mem.last_used else None
                }
                for track_id, track_mem in self.tracks.items()
            },
            'clips': {
                str(clip_id): {
                    'clip_id': clip_mem.clip_id,
                    'track_id': clip_mem.track_id,
                    'name': clip_mem.name,
                    'length_bars': clip_mem.length_bars,
                    'created_at': clip_mem.created_at.isoformat(),
                    'last_used': clip_mem.last_used.isoformat() if clip_mem.last_used else None
                }
                for clip_id, clip_mem in self.clips.items()
            },
            'devices': {
                str(device_id): {
                    'device_id': device_mem.device_id,
                    'track_id': device_mem.track_id,
                    'name': device_mem.name,
                    'device_type': device_mem.device_type,
                    'created_at': device_mem.created_at.isoformat(),
                    'parameters': device_mem.parameters
                }
                for device_id, device_mem in self.devices.items()
            }
        }
        return json.dumps(state, indent=2)
        
    def import_state(self, state_json: str) -> None:
        """
        Import memory state from JSON.
        
        Args:
            state_json: JSON string of memory state
        """
        try:
            state = json.loads(state_json)
            
            # Clear current state
            self.tracks.clear()
            self.clips.clear()
            self.devices.clear()
            self.name_to_track_id.clear()
            
            # Import tracks
            for track_id_str, track_data in state.get('tracks', {}).items():
                track_id = int(track_id_str)
                track_mem = TrackMemory(
                    track_id=track_data['track_id'],
                    name=track_data['name'],
                    track_type=track_data['track_type'],
                    created_at=datetime.fromisoformat(track_data['created_at']),
                    devices=track_data['devices'],
                    clips=track_data['clips'],
                    last_used=datetime.fromisoformat(track_data['last_used']) if track_data['last_used'] else None
                )
                self.tracks[track_id] = track_mem
                self.name_to_track_id[track_mem.name.lower()] = track_id
            
            # Import clips
            for clip_id_str, clip_data in state.get('clips', {}).items():
                clip_id = int(clip_id_str)
                self.clips[clip_id] = ClipMemory(
                    clip_id=clip_data['clip_id'],
                    track_id=clip_data['track_id'],
                    name=clip_data['name'],
                    length_bars=clip_data['length_bars'],
                    created_at=datetime.fromisoformat(clip_data['created_at']),
                    last_used=datetime.fromisoformat(clip_data['last_used']) if clip_data['last_used'] else None
                )
            
            # Import devices
            for device_id_str, device_data in state.get('devices', {}).items():
                device_id = int(device_id_str)
                self.devices[device_id] = DeviceMemory(
                    device_id=device_data['device_id'],
                    track_id=device_data['track_id'],
                    name=device_data['name'],
                    device_type=device_data['device_type'],
                    created_at=datetime.fromisoformat(device_data['created_at']),
                    parameters=device_data['parameters']
                )
                
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise ValueError(f"Invalid memory state JSON: {e}")