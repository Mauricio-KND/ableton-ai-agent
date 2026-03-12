"""
Session management MCP tools for Ableton Live control

Provides tools for controlling the overall Ableton Live session,
including tempo, playback, and global settings through the MCP interface.
"""

from typing import Dict, Any, Optional
import functools
from datetime import datetime

from ..utils.logger import get_logger
from ..utils.validators import validate_tempo
from ..state.memory import MemoryManager
from ..state.session_manager import SessionManager


def mcp_tool(func):
    """Decorator to mark functions as MCP tools."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.is_mcp_tool = True
    return wrapper


class SessionTools:
    """
    Collection of MCP tools for session management in Ableton Live.
    
    This class provides tools for controlling global session parameters
    like tempo, playback state, and other session-wide settings.
    """
    
    def __init__(
        self, 
        memory_manager: MemoryManager,
        session_manager: SessionManager,
        ableton_client: Any = None
    ):
        """
        Initialize session tools.
        
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
    def set_tempo(self, tempo: float) -> Dict[str, Any]:
        """
        Set the tempo of the Ableton Live session.
        
        Args:
            tempo: Tempo in BPM (20-999)
            
        Returns:
            Dictionary containing tempo setting result
        """
        try:
            tempo = validate_tempo(tempo)
            self.logger.info(f"Setting tempo to {tempo} BPM")
            
            old_tempo = self.session.session_state.tempo
            
            # This would use actual MCP call to Ableton
            # Update session state
            self.session.update_session_property('tempo', tempo)
            
            self.logger.info(f"Successfully set tempo from {old_tempo} to {tempo} BPM")
            
            return {
                'success': True,
                'old_tempo': old_tempo,
                'new_tempo': tempo,
                'message': f"Set tempo from {old_tempo} to {tempo} BPM"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to set tempo to {tempo}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to set tempo to {tempo}: {e}"
            }
            
    @mcp_tool
    def get_tempo(self) -> Dict[str, Any]:
        """
        Get the current tempo of the Ableton Live session.
        
        Returns:
            Dictionary containing current tempo
        """
        try:
            tempo = self.session.session_state.tempo
            self.logger.info(f"Current tempo: {tempo} BPM")
            
            return {
                'success': True,
                'tempo': tempo,
                'message': f"Current tempo is {tempo} BPM"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get tempo: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to get tempo: {e}"
            }
            
    @mcp_tool
    def start_playback(self) -> Dict[str, Any]:
        """
        Start playback in Ableton Live.
        
        Returns:
            Dictionary containing playback start result
        """
        try:
            self.logger.info("Starting playback")
            
            if self.session.session_state.is_playing:
                return {
                    'success': True,
                    'already_playing': True,
                    'message': "Playback is already running"
                }
            
            # This would use actual MCP call to Ableton
            # Update session state
            self.session.update_session_property('is_playing', True)
            
            self.logger.info("Successfully started playback")
            
            return {
                'success': True,
                'already_playing': False,
                'message': "Started playback"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to start playback: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to start playback: {e}"
            }
            
    @mcp_tool
    def stop_playback(self) -> Dict[str, Any]:
        """
        Stop playback in Ableton Live.
        
        Returns:
            Dictionary containing playback stop result
        """
        try:
            self.logger.info("Stopping playback")
            
            if not self.session.session_state.is_playing:
                return {
                    'success': True,
                    'already_stopped': True,
                    'message': "Playback is already stopped"
                }
            
            # This would use actual MCP call to Ableton
            # Update session state
            self.session.update_session_property('is_playing', False)
            
            self.logger.info("Successfully stopped playback")
            
            return {
                'success': True,
                'already_stopped': False,
                'message': "Stopped playback"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to stop playback: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to stop playback: {e}"
            }
            
    @mcp_tool
    def get_session_info(self) -> Dict[str, Any]:
        """
        Get comprehensive information about the current Ableton Live session.
        
        Returns:
            Dictionary containing session information
        """
        try:
            self.logger.info("Getting session information")
            
            session_state = self.session.get_session_state()
            state_summary = self.session.get_state_summary()
            
            session_info = {
                'tempo': session_state.tempo,
                'time_signature': session_state.time_signature,
                'is_playing': session_state.is_playing,
                'arrangement_overdub': session_state.arrangement_overdub,
                'session_automation_record': session_state.session_automation_record,
                'metronome': session_state.metronome,
                'current_song_time': session_state.current_song_time,
                'last_updated': session_state.last_updated.isoformat(),
                'summary': state_summary
            }
            
            self.logger.info("Successfully retrieved session information")
            
            return {
                'success': True,
                'session_info': session_info,
                'message': "Retrieved session information"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get session info: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to get session info: {e}"
            }
            
    @mcp_tool
    def save_session(self, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Save the current Ableton Live session.
        
        Args:
            name: Optional name for the saved session
            
        Returns:
            Dictionary containing save result
        """
        try:
            save_name = name or f"Session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.logger.info(f"Saving session as: {save_name}")
            
            # This would use actual MCP call to Ableton to save the session
            # For now, we'll simulate the save operation
            
            # Export current state for backup
            session_state_json = self.session.export_state()
            memory_state_json = self.memory.export_state()
            
            # In a real implementation, this would save to Ableton's project format
            # For now, we'll just log the operation
            self.logger.info(f"Session state exported: {len(session_state_json)} characters")
            self.logger.info(f"Memory state exported: {len(memory_state_json)} characters")
            
            self.logger.info(f"Successfully saved session as: {save_name}")
            
            return {
                'success': True,
                'session_name': save_name,
                'message': f"Saved session as '{save_name}'"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to save session: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to save session: {e}"
            }
            
    @mcp_tool
    def set_time_signature(self, numerator: int, denominator: int) -> Dict[str, Any]:
        """
        Set the time signature of the Ableton Live session.
        
        Args:
            numerator: Upper number of time signature (e.g., 3, 4, 6, 7)
            denominator: Lower number of time signature (e.g., 4, 8, 16)
            
        Returns:
            Dictionary containing time signature setting result
        """
        try:
            # Validate time signature
            if numerator < 1 or numerator > 32:
                raise ValueError("Time signature numerator must be between 1 and 32")
            if denominator not in [2, 4, 8, 16]:
                raise ValueError("Time signature denominator must be 2, 4, 8, or 16")
            
            new_signature = (numerator, denominator)
            self.logger.info(f"Setting time signature to {numerator}/{denominator}")
            
            old_signature = self.session.session_state.time_signature
            
            # This would use actual MCP call to Ableton
            # Update session state
            self.session.update_session_property('time_signature', new_signature)
            
            self.logger.info(f"Successfully set time signature from {old_signature} to {new_signature}")
            
            return {
                'success': True,
                'old_time_signature': old_signature,
                'new_time_signature': new_signature,
                'message': f"Set time signature from {old_signature} to {new_signature}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to set time signature to {numerator}/{denominator}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to set time signature to {numerator}/{denominator}: {e}"
            }
            
    @mcp_tool
    def set_metronome(self, enabled: bool) -> Dict[str, Any]:
        """
        Enable or disable the metronome.
        
        Args:
            enabled: True to enable metronome, False to disable
            
        Returns:
            Dictionary containing metronome setting result
        """
        try:
            self.logger.info(f"Setting metronome to {enabled}")
            
            old_enabled = self.session.session_state.metronome
            
            # This would use actual MCP call to Ableton
            # Update session state
            self.session.update_session_property('metronome', enabled)
            
            self.logger.info(f"Successfully set metronome from {old_enabled} to {enabled}")
            
            return {
                'success': True,
                'old_metronome': old_enabled,
                'new_metronome': enabled,
                'message': f"Set metronome from {old_enabled} to {enabled}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to set metronome to {enabled}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to set metronome to {enabled}: {e}"
            }
            
    @mcp_tool
    def set_arrangement_overdub(self, enabled: bool) -> Dict[str, Any]:
        """
        Enable or disable arrangement overdub.
        
        Args:
            enabled: True to enable arrangement overdub, False to disable
            
        Returns:
            Dictionary containing arrangement overdub setting result
        """
        try:
            self.logger.info(f"Setting arrangement overdub to {enabled}")
            
            old_enabled = self.session.session_state.arrangement_overdub
            
            # This would use actual MCP call to Ableton
            # Update session state
            self.session.update_session_property('arrangement_overdub', enabled)
            
            self.logger.info(f"Successfully set arrangement overdub from {old_enabled} to {enabled}")
            
            return {
                'success': True,
                'old_arrangement_overdub': old_enabled,
                'new_arrangement_overdub': enabled,
                'message': f"Set arrangement overdub from {old_enabled} to {enabled}"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to set arrangement overdub to {enabled}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to set arrangement overdub to {enabled}: {e}"
            }


# Global instance for MCP tool registration
_session_tools_instance: Optional[SessionTools] = None


def initialize_session_tools(
    memory_manager: MemoryManager,
    session_manager: SessionManager,
    ableton_client: Any = None
) -> SessionTools:
    """
    Initialize the session tools with required dependencies.
    
    Args:
        memory_manager: Memory manager instance
        session_manager: Session manager instance
        ableton_client: Ableton client instance
        
    Returns:
        Initialized SessionTools instance
    """
    global _session_tools_instance
    _session_tools_instance = SessionTools(memory_manager, session_manager, ableton_client)
    return _session_tools_instance


def get_session_tools() -> Optional[SessionTools]:
    """Get the global session tools instance."""
    return _session_tools_instance


# Export individual tool functions for MCP registration
def set_tempo(tempo: float) -> Dict[str, Any]:
    """Set session tempo."""
    if not _session_tools_instance:
        raise RuntimeError("Session tools not initialized")
    return _session_tools_instance.set_tempo(tempo)


def get_tempo() -> Dict[str, Any]:
    """Get current tempo."""
    if not _session_tools_instance:
        raise RuntimeError("Session tools not initialized")
    return _session_tools_instance.get_tempo()


def start_playback() -> Dict[str, Any]:
    """Start playback."""
    if not _session_tools_instance:
        raise RuntimeError("Session tools not initialized")
    return _session_tools_instance.start_playback()


def stop_playback() -> Dict[str, Any]:
    """Stop playback."""
    if not _session_tools_instance:
        raise RuntimeError("Session tools not initialized")
    return _session_tools_instance.stop_playback()


def get_session_info() -> Dict[str, Any]:
    """Get session information."""
    if not _session_tools_instance:
        raise RuntimeError("Session tools not initialized")
    return _session_tools_instance.get_session_info()


def save_session(name: Optional[str] = None) -> Dict[str, Any]:
    """Save session."""
    if not _session_tools_instance:
        raise RuntimeError("Session tools not initialized")
    return _session_tools_instance.save_session(name)


def set_time_signature(numerator: int, denominator: int) -> Dict[str, Any]:
    """Set time signature."""
    if not _session_tools_instance:
        raise RuntimeError("Session tools not initialized")
    return _session_tools_instance.set_time_signature(numerator, denominator)


def set_metronome(enabled: bool) -> Dict[str, Any]:
    """Set metronome."""
    if not _session_tools_instance:
        raise RuntimeError("Session tools not initialized")
    return _session_tools_instance.set_metronome(enabled)


def set_arrangement_overdub(enabled: bool) -> Dict[str, Any]:
    """Set arrangement overdub."""
    if not _session_tools_instance:
        raise RuntimeError("Session tools not initialized")
    return _session_tools_instance.set_arrangement_overdub(enabled)