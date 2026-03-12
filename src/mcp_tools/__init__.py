"""
MCP Tools for Ableton Live Control

This module contains all the MCP (Model Context Protocol) tools that allow
the AI agent to control Ableton Live through a structured, extensible interface.
"""

from .track_tools import *
from .device_tools import *
from .clip_tools import *
from .session_tools import *

__all__ = [
    # Track management tools
    'create_midi_track',
    'create_audio_track', 
    'delete_track',
    'set_track_name',
    'set_track_volume',
    'set_track_mute',
    'get_track_info',
    
    # Device management tools
    'add_device',
    'remove_device',
    'set_device_parameter',
    'get_device_info',
    
    # Clip and MIDI tools
    'create_midi_clip',
    'delete_clip',
    'fire_clip',
    'stop_clip',
    'add_midi_notes',
    'clear_clip_notes',
    
    # Session management tools
    'set_tempo',
    'get_tempo',
    'get_session_info',
    'save_session',
    'start_playback',
    'stop_playback'
]