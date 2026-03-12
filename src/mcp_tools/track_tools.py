"""
Track management MCP tools for Ableton Live control

Provides tools for creating, modifying, and managing tracks in Ableton Live
through the MCP (Model Context Protocol) interface.
"""

from typing import Dict, Any, Optional, List
import functools

from ..utils.logger import get_logger
from ..utils.validators import (
    validate_track_id, validate_track_name, validate_volume
)
from ..state.memory import MemoryManager
from ..state.session_manager import SessionManager


def mcp_tool(func):
    """Decorator to mark functions as MCP tools."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.is_mcp_tool = True
    return wrapper


class TrackTools:
    """
    Collection of MCP tools for track management in Ableton Live.
    
    This class provides a comprehensive set of tools for creating,
    modifying, and managing tracks through the MCP interface.
    """
    
    def __init__(
        self, 
        memory_manager: MemoryManager,
        session_manager: SessionManager,
        ableton_client: Any = None
    ):
        """
        Initialize track tools.
        
        Args:
            memory_manager: Memory manager for tracking created elements
            session_manager: Session manager for state tracking
            ableton_client: Client for communicating with Ableton
        """
        self.logger = get_logger(__name__)
        self.memory = memory_manager
        self.session = session_manager
        self.ableton = ableton_client
        
    @mcp_tool
    def create_midi_track(self, name: str) -> Dict[str, Any]:
        """
        Create a new MIDI track in Ableton Live.
        
        Args:
            name: Name for the new track
            
        Returns:
            Dictionary containing track creation result
        """
        try:
            name = validate_track_name(name)
            self.logger.info(f"Creating MIDI track: {name}")
            
            # This would use actual MCP call to Ableton
            # For now, we'll simulate the response
            track_id = len(self.session.tracks)  # Simulated track ID
            
            # Update session state
            from ..state.session_manager import TrackState
            self.session.tracks[track_id] = TrackState(
                track_id=track_id,
                name=name,
                track_type='midi'
            )
            
            # Update memory
            self.memory.add_track(track_id, name, 'midi')
            
            self.logger.info(f"Successfully created MIDI track '{name}' with ID {track_id}")
            
            return {
                'success': True,
                'track_id': track_id,
                'name': name,
                'track_type': 'midi',
                'message': f"Created MIDI track '{name}' with ID {track_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create MIDI track '{name}': {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create MIDI track '{name}': {e}"
            }
            
    @mcp_tool
    def create_audio_track(self, name: str) -> Dict[str, Any]:
        """
        Create a new audio track in Ableton Live.
        
        Args:
            name: Name for the new track
            
        Returns:
            Dictionary containing track creation result
        """
        try:
            name = validate_track_name(name)
            self.logger.info(f"Creating audio track: {name}")
            
            # This would use actual MCP call to Ableton
            track_id = len(self.session.tracks)  # Simulated track ID
            
            # Update session state
            from ..state.session_manager import TrackState
            self.session.tracks[track_id] = TrackState(
                track_id=track_id,
                name=name,
                track_type='audio'
            )
            
            # Update memory
            self.memory.add_track(track_id, name, 'audio')
            
            self.logger.info(f"Successfully created audio track '{name}' with ID {track_id}")
            
            return {
                'success': True,
                'track_id': track_id,
                'name': name,
                'track_type': 'audio',
                'message': f"Created audio track '{name}' with ID {track_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create audio track '{name}': {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create audio track '{name}': {e}"
            }
            
    @mcp_tool
    def delete_track(self, track_id: int) -> Dict[str, Any]:
        """
        Delete a track from Ableton Live.
        
        Args:
            track_id: ID of the track to delete
            
        Returns:
            Dictionary containing deletion result
        """
        try:
            track_id = validate_track_id(track_id)
            self.logger.info(f"Deleting track {track_id}")
            
            # Check if track exists
            if track_id not in self.session.tracks:
                raise ValueError(f"Track {track_id} not found")
            
            track_name = self.session.tracks[track_id].name
            
            # This would use actual MCP call to Ableton
            # Simulate deletion
            del self.session.tracks[track_id]
            
            # Update memory
            self.memory.remove_track(track_id)
            
            self.logger.info(f"Successfully deleted track '{track_name}' (ID {track_id})")
            
            return {
                'success': True,
                'track_id': track_id,
                'track_name': track_name,
                'message': f"Deleted track '{track_name}' (ID {track_id})"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to delete track {track_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to delete track {track_id}: {e}"
            }
            
    @mcp_tool
    def set_track_name(self, track_id: int, name: str) -> Dict[str, Any]:
        """
        Set the name of a track.
        
        Args:
            track_id: ID of the track to rename
            name: New name for the track
            
        Returns:
            Dictionary containing rename result
        """
        try:
            track_id = validate_track_id(track_id)
            name = validate_track_name(name)
            self.logger.info(f"Renaming track {track_id} to '{name}'")
            
            # Check if track exists
            if track_id not in self.session.tracks:
                raise ValueError(f"Track {track_id} not found")
            
            old_name = self.session.tracks[track_id].name
            
            # This would use actual MCP call to Ableton
            # Update session state
            self.session.tracks[track_id].name = name
            self.session.tracks[track_id].last_updated
            
            # Update memory
            self.memory.remove_track(track_id)
            self.memory.add_track(track_id, name, self.session.tracks[track_id].track_type)
            
            self.logger.info(f"Successfully renamed track {track_id} from '{old_name}' to '{name}'")
            
            return {
                'success': True,
                'track_id': track_id,
                'old_name': old_name,
                'new_name': name,
                'message': f"Renamed track {track_id} from '{old_name}' to '{name}'"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to rename track {track_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to rename track {track_id}: {e}"
            }
            
    @mcp_tool
    def set_track_volume(self, track_id: int, volume: float) -> Dict[str, Any]:
        """
        Set the volume of a track.
        
        Args:
            track_id: ID of the track
            volume: Volume level (0.0 to 1.0)
            
        Returns:
            Dictionary containing volume setting result
        """
        try:
            track_id = validate_track_id(track_id)
            volume = validate_volume(volume)
            self.logger.info(f"Setting volume of track {track_id} to {volume}")
            
            # Check if track exists
            if track_id not in self.session.tracks:
                raise ValueError(f"Track {track_id} not found")
            
            old_volume = self.session.tracks[track_id].volume
            
            # This would use actual MCP call to Ableton
            # Update session state
            self.session.update_track_state(track_id, volume=volume)
            
            # Update memory usage
            self.memory.update_track_usage(track_id)
            
            self.logger.info(f"Successfully set volume of track {track_id} from {old_volume} to {volume}")
            
            return {
                'success': True,
                'track_id': track_id,
                'old_volume': old_volume,
                'new_volume': volume,
                'message': f"Set volume of track {track_id} from {old_volume} to {volume}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to set volume of track {track_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to set volume of track {track_id}: {e}"
            }
            
    @mcp_tool
    def set_track_mute(self, track_id: int, mute: bool) -> Dict[str, Any]:
        """
        Set the mute state of a track.
        
        Args:
            track_id: ID of the track
            mute: True to mute, False to unmute
            
        Returns:
            Dictionary containing mute setting result
        """
        try:
            track_id = validate_track_id(track_id)
            self.logger.info(f"Setting mute state of track {track_id} to {mute}")
            
            # Check if track exists
            if track_id not in self.session.tracks:
                raise ValueError(f"Track {track_id} not found")
            
            old_mute = self.session.tracks[track_id].mute
            
            # This would use actual MCP call to Ableton
            # Update session state
            self.session.update_track_state(track_id, mute=mute)
            
            # Update memory usage
            self.memory.update_track_usage(track_id)
            
            self.logger.info(f"Successfully set mute state of track {track_id} from {old_mute} to {mute}")
            
            return {
                'success': True,
                'track_id': track_id,
                'old_mute': old_mute,
                'new_mute': mute,
                'message': f"Set mute state of track {track_id} from {old_mute} to {mute}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to set mute state of track {track_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to set mute state of track {track_id}: {e}"
            }
            
    @mcp_tool
    def get_track_info(self, track_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a track.
        
        Args:
            track_id: ID of the track
            
        Returns:
            Dictionary containing track information
        """
        try:
            track_id = validate_track_id(track_id)
            
            # Get track state
            track_state = self.session.get_track_state(track_id)
            if not track_state:
                raise ValueError(f"Track {track_id} not found")
            
            # Get memory information
            memory_info = self.memory.tracks.get(track_id)
            
            track_info = {
                'track_id': track_state.track_id,
                'name': track_state.name,
                'track_type': track_state.track_type,
                'volume': track_state.volume,
                'pan': track_state.pan,
                'mute': track_state.mute,
                'solo': track_state.solo,
                'armed': track_state.armed,
                'is_playing': track_state.is_playing,
                'clip_count': track_state.clip_count,
                'device_count': track_state.device_count,
                'last_updated': track_state.last_updated.isoformat()
            }
            
            # Add memory information if available
            if memory_info:
                track_info['memory'] = {
                    'created_at': memory_info.created_at.isoformat(),
                    'devices': memory_info.devices,
                    'clips': memory_info.clips,
                    'last_used': memory_info.last_used.isoformat() if memory_info.last_used else None
                }
            
            self.logger.info(f"Retrieved information for track {track_id}")
            
            return {
                'success': True,
                'track_info': track_info,
                'message': f"Retrieved information for track {track_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get track info for {track_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to get track info for {track_id}: {e}"
            }
            
    @mcp_tool
    def list_tracks(self, track_type: Optional[str] = None) -> Dict[str, Any]:
        """
        List all tracks, optionally filtered by type.
        
        Args:
            track_type: Optional filter by track type ('midi', 'audio', 'return', 'master')
            
        Returns:
            Dictionary containing list of tracks
        """
        try:
            self.logger.info(f"Listing tracks with type filter: {track_type}")
            
            if track_type:
                tracks = self.session.get_tracks_by_type(track_type)
            else:
                tracks = list(self.session.tracks.values())
            
            track_list = []
            for track in tracks:
                track_info = {
                    'track_id': track.track_id,
                    'name': track.name,
                    'track_type': track.track_type,
                    'volume': track.volume,
                    'mute': track.mute,
                    'solo': track.solo,
                    'is_playing': track.is_playing,
                    'clip_count': track.clip_count,
                    'device_count': track.device_count
                }
                track_list.append(track_info)
            
            self.logger.info(f"Found {len(track_list)} tracks")
            
            return {
                'success': True,
                'tracks': track_list,
                'count': len(track_list),
                'filter': track_type,
                'message': f"Found {len(track_list)} tracks" + (f" of type '{track_type}'" if track_type else "")
            }
            
        except Exception as e:
            self.logger.error(f"Failed to list tracks: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to list tracks: {e}"
            }


# Global instance for MCP tool registration
_track_tools_instance: Optional[TrackTools] = None


def initialize_track_tools(
    memory_manager: MemoryManager,
    session_manager: SessionManager,
    ableton_client: Any = None
) -> TrackTools:
    """
    Initialize the track tools with required dependencies.
    
    Args:
        memory_manager: Memory manager instance
        session_manager: Session manager instance
        ableton_client: Ableton client instance
        
    Returns:
        Initialized TrackTools instance
    """
    global _track_tools_instance
    _track_tools_instance = TrackTools(memory_manager, session_manager, ableton_client)
    return _track_tools_instance


def get_track_tools() -> Optional[TrackTools]:
    """Get the global track tools instance."""
    return _track_tools_instance


# Export individual tool functions for MCP registration
def create_midi_track(name: str) -> Dict[str, Any]:
    """Create a new MIDI track."""
    if not _track_tools_instance:
        raise RuntimeError("Track tools not initialized")
    return _track_tools_instance.create_midi_track(name)


def create_audio_track(name: str) -> Dict[str, Any]:
    """Create a new audio track."""
    if not _track_tools_instance:
        raise RuntimeError("Track tools not initialized")
    return _track_tools_instance.create_audio_track(name)


def delete_track(track_id: int) -> Dict[str, Any]:
    """Delete a track."""
    if not _track_tools_instance:
        raise RuntimeError("Track tools not initialized")
    return _track_tools_instance.delete_track(track_id)


def set_track_name(track_id: int, name: str) -> Dict[str, Any]:
    """Set track name."""
    if not _track_tools_instance:
        raise RuntimeError("Track tools not initialized")
    return _track_tools_instance.set_track_name(track_id, name)


def set_track_volume(track_id: int, volume: float) -> Dict[str, Any]:
    """Set track volume."""
    if not _track_tools_instance:
        raise RuntimeError("Track tools not initialized")
    return _track_tools_instance.set_track_volume(track_id, volume)


def set_track_mute(track_id: int, mute: bool) -> Dict[str, Any]:
    """Set track mute state."""
    if not _track_tools_instance:
        raise RuntimeError("Track tools not initialized")
    return _track_tools_instance.set_track_mute(track_id, mute)


def get_track_info(track_id: int) -> Dict[str, Any]:
    """Get track information."""
    if not _track_tools_instance:
        raise RuntimeError("Track tools not initialized")
    return _track_tools_instance.get_track_info(track_id)


def list_tracks(track_type: Optional[str] = None) -> Dict[str, Any]:
    """List tracks."""
    if not _track_tools_instance:
        raise RuntimeError("Track tools not initialized")
    return _track_tools_instance.list_tracks(track_type)