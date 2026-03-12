"""
Clip management MCP tools for Ableton Live control

Provides tools for creating, modifying, and managing clips in Ableton Live
through the MCP (Model Context Protocol) interface.
"""

from typing import Dict, Any, Optional, List
import functools

from ..utils.logger import get_logger
from ..utils.validators import (
    validate_track_id, validate_clip_length, validate_midi_notes
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


class ClipTools:
    """
    Collection of MCP tools for clip management in Ableton Live.
    
    This class provides tools for creating, modifying, and managing
    MIDI and audio clips through the MCP interface.
    """
    
    def __init__(
        self, 
        memory_manager: MemoryManager,
        session_manager: SessionManager,
        ableton_client: Any = None
    ):
        """
        Initialize clip tools.
        
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
    def create_midi_clip(self, track_id: int, length_bars: int, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new MIDI clip in a track.
        
        Args:
            track_id: ID of the track to create the clip in
            length_bars: Length of the clip in bars
            name: Optional name for the clip
            
        Returns:
            Dictionary containing clip creation result
        """
        try:
            track_id = validate_track_id(track_id)
            length_bars = validate_clip_length(length_bars)
            
            # Check if track exists
            if track_id not in self.session.tracks:
                raise ValueError(f"Track {track_id} not found")
            
            track = self.session.tracks[track_id]
            if track.track_type != 'midi':
                raise ValueError(f"Track {track_id} is not a MIDI track")
            
            clip_name = name or f"MIDI Clip {len(self.session.clips) + 1}"
            self.logger.info(f"Creating MIDI clip '{clip_name}' in track {track_id} ({length_bars} bars)")
            
            # This would use actual MCP call to Ableton
            # Simulate clip creation
            clip_id = len(self.session.clips)  # Simulated clip ID
            
            # Update session state
            from ..state.session_manager import ClipState
            self.session.clips[clip_id] = ClipState(
                clip_id=clip_id,
                track_id=track_id,
                name=clip_name,
                length_bars=length_bars
            )
            
            # Update track state
            track.clip_count += 1
            
            # Update memory
            self.memory.add_clip(clip_id, track_id, clip_name, length_bars)
            
            self.logger.info(f"Successfully created MIDI clip '{clip_name}' with ID {clip_id}")
            
            return {
                'success': True,
                'clip_id': clip_id,
                'track_id': track_id,
                'name': clip_name,
                'length_bars': length_bars,
                'message': f"Created MIDI clip '{clip_name}' (ID {clip_id}) in track {track_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create MIDI clip: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create MIDI clip: {e}"
            }
            
    @mcp_tool
    def delete_clip(self, track_id: int, clip_id: int) -> Dict[str, Any]:
        """
        Delete a clip from a track.
        
        Args:
            track_id: ID of the track containing the clip
            clip_id: ID of the clip to delete
            
        Returns:
            Dictionary containing deletion result
        """
        try:
            track_id = validate_track_id(track_id)
            self.logger.info(f"Deleting clip {clip_id} from track {track_id}")
            
            # Check if clip exists
            if clip_id not in self.session.clips:
                raise ValueError(f"Clip {clip_id} not found")
            
            clip = self.session.clips[clip_id]
            if clip.track_id != track_id:
                raise ValueError(f"Clip {clip_id} is not in track {track_id}")
            
            clip_name = clip.name
            
            # This would use actual MCP call to Ableton
            # Simulate deletion
            del self.session.clips[clip_id]
            
            # Update track state
            if track_id in self.session.tracks:
                self.session.tracks[track_id].clip_count = max(0, self.session.tracks[track_id].clip_count - 1)
            
            # Update memory
            if clip_id in self.memory.clips:
                del self.memory.clips[clip_id]
            
            self.logger.info(f"Successfully deleted clip '{clip_name}' (ID {clip_id}) from track {track_id}")
            
            return {
                'success': True,
                'clip_id': clip_id,
                'track_id': track_id,
                'clip_name': clip_name,
                'message': f"Deleted clip '{clip_name}' (ID {clip_id}) from track {track_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to delete clip {clip_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to delete clip {clip_id}: {e}"
            }
            
    @mcp_tool
    def fire_clip(self, track_id: int, clip_id: int) -> Dict[str, Any]:
        """
        Fire (launch) a clip.
        
        Args:
            track_id: ID of the track containing the clip
            clip_id: ID of the clip to fire
            
        Returns:
            Dictionary containing fire result
        """
        try:
            track_id = validate_track_id(track_id)
            self.logger.info(f"Firing clip {clip_id} in track {track_id}")
            
            # Check if clip exists
            if clip_id not in self.session.clips:
                raise ValueError(f"Clip {clip_id} not found")
            
            clip = self.session.clips[clip_id]
            if clip.track_id != track_id:
                raise ValueError(f"Clip {clip_id} is not in track {track_id}")
            
            # This would use actual MCP call to Ableton
            # Update session state
            clip.is_playing = True
            clip.is_triggered = True
            clip.last_updated
            
            # Update memory usage
            self.memory.update_track_usage(track_id)
            
            self.logger.info(f"Successfully fired clip {clip_id} in track {track_id}")
            
            return {
                'success': True,
                'clip_id': clip_id,
                'track_id': track_id,
                'clip_name': clip.name,
                'message': f"Fired clip '{clip.name}' (ID {clip_id}) in track {track_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to fire clip {clip_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to fire clip {clip_id}: {e}"
            }
            
    @mcp_tool
    def stop_clip(self, track_id: int, clip_id: int) -> Dict[str, Any]:
        """
        Stop a playing clip.
        
        Args:
            track_id: ID of the track containing the clip
            clip_id: ID of the clip to stop
            
        Returns:
            Dictionary containing stop result
        """
        try:
            track_id = validate_track_id(track_id)
            self.logger.info(f"Stopping clip {clip_id} in track {track_id}")
            
            # Check if clip exists
            if clip_id not in self.session.clips:
                raise ValueError(f"Clip {clip_id} not found")
            
            clip = self.session.clips[clip_id]
            if clip.track_id != track_id:
                raise ValueError(f"Clip {clip_id} is not in track {track_id}")
            
            # This would use actual MCP call to Ableton
            # Update session state
            clip.is_playing = False
            clip.is_triggered = False
            clip.last_updated
            
            self.logger.info(f"Successfully stopped clip {clip_id} in track {track_id}")
            
            return {
                'success': True,
                'clip_id': clip_id,
                'track_id': track_id,
                'clip_name': clip.name,
                'message': f"Stopped clip '{clip.name}' (ID {clip_id}) in track {track_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to stop clip {clip_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to stop clip {clip_id}: {e}"
            }
            
    @mcp_tool
    def add_midi_notes(self, track_id: int, clip_id: int, notes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add MIDI notes to a clip.
        
        Args:
            track_id: ID of the track containing the clip
            clip_id: ID of the clip to add notes to
            notes: List of MIDI note dictionaries
            
        Returns:
            Dictionary containing note addition result
        """
        try:
            track_id = validate_track_id(track_id)
            notes = validate_midi_notes(notes)
            
            self.logger.info(f"Adding {len(notes)} MIDI notes to clip {clip_id} in track {track_id}")
            
            # Check if clip exists
            if clip_id not in self.session.clips:
                raise ValueError(f"Clip {clip_id} not found")
            
            clip = self.session.clips[clip_id]
            if clip.track_id != track_id:
                raise ValueError(f"Clip {clip_id} is not in track {track_id}")
            
            # This would use actual MCP call to Ableton to add notes
            # For now, we'll just validate and log the operation
            
            # Update memory usage
            self.memory.update_track_usage(track_id)
            
            self.logger.info(f"Successfully added {len(notes)} MIDI notes to clip {clip_id}")
            
            return {
                'success': True,
                'clip_id': clip_id,
                'track_id': track_id,
                'notes_added': len(notes),
                'notes': notes,
                'message': f"Added {len(notes)} MIDI notes to clip {clip_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to add MIDI notes to clip {clip_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to add MIDI notes to clip {clip_id}: {e}"
            }
            
    @mcp_tool
    def clear_clip_notes(self, track_id: int, clip_id: int) -> Dict[str, Any]:
        """
        Clear all notes from a MIDI clip.
        
        Args:
            track_id: ID of the track containing the clip
            clip_id: ID of the clip to clear
            
        Returns:
            Dictionary containing clear result
        """
        try:
            track_id = validate_track_id(track_id)
            self.logger.info(f"Clearing notes from clip {clip_id} in track {track_id}")
            
            # Check if clip exists
            if clip_id not in self.session.clips:
                raise ValueError(f"Clip {clip_id} not found")
            
            clip = self.session.clips[clip_id]
            if clip.track_id != track_id:
                raise ValueError(f"Clip {clip_id} is not in track {track_id}")
            
            # This would use actual MCP call to Ableton to clear notes
            # For now, we'll just log the operation
            
            self.logger.info(f"Successfully cleared notes from clip {clip_id}")
            
            return {
                'success': True,
                'clip_id': clip_id,
                'track_id': track_id,
                'clip_name': clip.name,
                'message': f"Cleared all notes from clip '{clip.name}' (ID {clip_id})"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to clear notes from clip {clip_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to clear notes from clip {clip_id}: {e}"
            }
            
    @mcp_tool
    def get_clip_info(self, track_id: int, clip_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a clip.
        
        Args:
            track_id: ID of the track containing the clip
            clip_id: ID of the clip
            
        Returns:
            Dictionary containing clip information
        """
        try:
            track_id = validate_track_id(track_id)
            
            # Get clip state
            clip_state = self.session.get_clip_state(clip_id)
            if not clip_state:
                raise ValueError(f"Clip {clip_id} not found")
            
            if clip_state.track_id != track_id:
                raise ValueError(f"Clip {clip_id} is not in track {track_id}")
            
            # Get memory information
            memory_info = self.memory.clips.get(clip_id)
            
            clip_info = {
                'clip_id': clip_state.clip_id,
                'track_id': clip_state.track_id,
                'name': clip_state.name,
                'length_bars': clip_state.length_bars,
                'is_playing': clip_state.is_playing,
                'is_triggered': clip_state.is_triggered,
                'start_time': clip_state.start_time,
                'last_updated': clip_state.last_updated.isoformat()
            }
            
            # Add memory information if available
            if memory_info:
                clip_info['memory'] = {
                    'created_at': memory_info.created_at.isoformat(),
                    'last_used': memory_info.last_used.isoformat() if memory_info.last_used else None
                }
            
            self.logger.info(f"Retrieved information for clip {clip_id}")
            
            return {
                'success': True,
                'clip_info': clip_info,
                'message': f"Retrieved information for clip {clip_id}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get clip info for {clip_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to get clip info for {clip_id}: {e}"
            }
            
    @mcp_tool
    def list_clips(self, track_id: Optional[int] = None) -> Dict[str, Any]:
        """
        List all clips, optionally filtered by track.
        
        Args:
            track_id: Optional track ID to filter clips by
            
        Returns:
            Dictionary containing list of clips
        """
        try:
            self.logger.info(f"Listing clips with track filter: {track_id}")
            
            if track_id:
                track_id = validate_track_id(track_id)
                clips = [clip for clip in self.session.clips.values() if clip.track_id == track_id]
            else:
                clips = list(self.session.clips.values())
            
            clip_list = []
            for clip in clips:
                clip_info = {
                    'clip_id': clip.clip_id,
                    'track_id': clip.track_id,
                    'name': clip.name,
                    'length_bars': clip.length_bars,
                    'is_playing': clip.is_playing,
                    'is_triggered': clip.is_triggered
                }
                clip_list.append(clip_info)
            
            self.logger.info(f"Found {len(clip_list)} clips")
            
            return {
                'success': True,
                'clips': clip_list,
                'count': len(clip_list),
                'track_filter': track_id,
                'message': f"Found {len(clip_list)} clips" + (f" in track {track_id}" if track_id else "")
            }
            
        except Exception as e:
            self.logger.error(f"Failed to list clips: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to list clips: {e}"
            }


# Global instance for MCP tool registration
_clip_tools_instance: Optional[ClipTools] = None


def initialize_clip_tools(
    memory_manager: MemoryManager,
    session_manager: SessionManager,
    ableton_client: Any = None
) -> ClipTools:
    """
    Initialize the clip tools with required dependencies.
    
    Args:
        memory_manager: Memory manager instance
        session_manager: Session manager instance
        ableton_client: Ableton client instance
        
    Returns:
        Initialized ClipTools instance
    """
    global _clip_tools_instance
    _clip_tools_instance = ClipTools(memory_manager, session_manager, ableton_client)
    return _clip_tools_instance


def get_clip_tools() -> Optional[ClipTools]:
    """Get the global clip tools instance."""
    return _clip_tools_instance


# Export individual tool functions for MCP registration
def create_midi_clip(track_id: int, length_bars: int, name: Optional[str] = None) -> Dict[str, Any]:
    """Create a new MIDI clip."""
    if not _clip_tools_instance:
        raise RuntimeError("Clip tools not initialized")
    return _clip_tools_instance.create_midi_clip(track_id, length_bars, name)


def delete_clip(track_id: int, clip_id: int) -> Dict[str, Any]:
    """Delete a clip."""
    if not _clip_tools_instance:
        raise RuntimeError("Clip tools not initialized")
    return _clip_tools_instance.delete_clip(track_id, clip_id)


def fire_clip(track_id: int, clip_id: int) -> Dict[str, Any]:
    """Fire a clip."""
    if not _clip_tools_instance:
        raise RuntimeError("Clip tools not initialized")
    return _clip_tools_instance.fire_clip(track_id, clip_id)


def stop_clip(track_id: int, clip_id: int) -> Dict[str, Any]:
    """Stop a clip."""
    if not _clip_tools_instance:
        raise RuntimeError("Clip tools not initialized")
    return _clip_tools_instance.stop_clip(track_id, clip_id)


def add_midi_notes(track_id: int, clip_id: int, notes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Add MIDI notes to a clip."""
    if not _clip_tools_instance:
        raise RuntimeError("Clip tools not initialized")
    return _clip_tools_instance.add_midi_notes(track_id, clip_id, notes)


def clear_clip_notes(track_id: int, clip_id: int) -> Dict[str, Any]:
    """Clear notes from a clip."""
    if not _clip_tools_instance:
        raise RuntimeError("Clip tools not initialized")
    return _clip_tools_instance.clear_clip_notes(track_id, clip_id)


def get_clip_info(track_id: int, clip_id: int) -> Dict[str, Any]:
    """Get clip information."""
    if not _clip_tools_instance:
        raise RuntimeError("Clip tools not initialized")
    return _clip_tools_instance.get_clip_info(track_id, clip_id)


def list_clips(track_id: Optional[int] = None) -> Dict[str, Any]:
    """List clips."""
    if not _clip_tools_instance:
        raise RuntimeError("Clip tools not initialized")
    return _clip_tools_instance.list_clips(track_id)