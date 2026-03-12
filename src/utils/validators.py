"""
Input validation utilities for the Ableton AI Agent

Provides validation functions for various input types to ensure
data integrity and prevent errors.
"""

import re
from typing import List, Dict, Any, Optional


def validate_track_id(track_id: Any) -> int:
    """
    Validate and normalize track ID.
    
    Args:
        track_id: Track ID to validate
        
    Returns:
        Validated track ID as integer
        
    Raises:
        ValueError: If track ID is invalid
    """
    try:
        track_id_int = int(track_id)
        if track_id_int < 0:
            raise ValueError("Track ID must be non-negative")
        return track_id_int
    except (ValueError, TypeError):
        raise ValueError(f"Invalid track ID: {track_id}. Must be a non-negative integer.")


def validate_device_name(device_name: Any) -> str:
    """
    Validate device name.
    
    Args:
        device_name: Device name to validate
        
    Returns:
        Validated device name as string
        
    Raises:
        ValueError: If device name is invalid
    """
    if not device_name:
        raise ValueError("Device name cannot be empty")
    
    device_name_str = str(device_name).strip()
    if not device_name_str:
        raise ValueError("Device name cannot be empty or whitespace")
    
    # Check for valid characters (alphanumeric, spaces, hyphens, underscores)
    if not re.match(r'^[a-zA-Z0-9\s\-_]+$', device_name_str):
        raise ValueError(f"Invalid device name: {device_name_str}. Only alphanumeric characters, spaces, hyphens, and underscores are allowed.")
    
    return device_name_str


def validate_midi_notes(notes: Any) -> List[Dict[str, Any]]:
    """
    Validate MIDI notes structure.
    
    Args:
        notes: MIDI notes to validate
        
    Returns:
        Validated list of MIDI note dictionaries
        
    Raises:
        ValueError: If notes structure is invalid
    """
    if not isinstance(notes, list):
        raise ValueError("MIDI notes must be a list")
    
    validated_notes = []
    for i, note in enumerate(notes):
        if not isinstance(note, dict):
            raise ValueError(f"Note {i} must be a dictionary")
        
        # Check required fields
        required_fields = ['pitch', 'velocity', 'start_time', 'duration']
        for field in required_fields:
            if field not in note:
                raise ValueError(f"Note {i} missing required field: {field}")
        
        # Validate pitch (0-127)
        try:
            pitch = int(note['pitch'])
            if not 0 <= pitch <= 127:
                raise ValueError(f"Note {i} pitch must be between 0 and 127")
            note['pitch'] = pitch
        except (ValueError, TypeError):
            raise ValueError(f"Note {i} pitch must be an integer between 0 and 127")
        
        # Validate velocity (0-127)
        try:
            velocity = int(note['velocity'])
            if not 0 <= velocity <= 127:
                raise ValueError(f"Note {i} velocity must be between 0 and 127")
            note['velocity'] = velocity
        except (ValueError, TypeError):
            raise ValueError(f"Note {i} velocity must be an integer between 0 and 127")
        
        # Validate start_time (non-negative)
        try:
            start_time = float(note['start_time'])
            if start_time < 0:
                raise ValueError(f"Note {i} start_time must be non-negative")
            note['start_time'] = start_time
        except (ValueError, TypeError):
            raise ValueError(f"Note {i} start_time must be a non-negative number")
        
        # Validate duration (positive)
        try:
            duration = float(note['duration'])
            if duration <= 0:
                raise ValueError(f"Note {i} duration must be positive")
            note['duration'] = duration
        except (ValueError, TypeError):
            raise ValueError(f"Note {i} duration must be a positive number")
        
        validated_notes.append(note)
    
    return validated_notes


def validate_tempo(tempo: Any) -> float:
    """
    Validate tempo value.
    
    Args:
        tempo: Tempo to validate
        
    Returns:
        Validated tempo as float
        
    Raises:
        ValueError: If tempo is invalid
    """
    try:
        tempo_float = float(tempo)
        if not 20 <= tempo_float <= 999:  # Ableton's tempo range
            raise ValueError("Tempo must be between 20 and 999 BPM")
        return tempo_float
    except (ValueError, TypeError):
        raise ValueError(f"Invalid tempo: {tempo}. Must be a number between 20 and 999.")


def validate_volume(volume: Any) -> float:
    """
    Validate volume value (0.0 to 1.0).
    
    Args:
        volume: Volume to validate
        
    Returns:
        Validated volume as float
        
    Raises:
        ValueError: If volume is invalid
    """
    try:
        volume_float = float(volume)
        if not 0.0 <= volume_float <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0")
        return volume_float
    except (ValueError, TypeError):
        raise ValueError(f"Invalid volume: {volume}. Must be a number between 0.0 and 1.0.")


def validate_clip_length(length_bars: Any) -> int:
    """
    Validate clip length in bars.
    
    Args:
        length_bars: Clip length to validate
        
    Returns:
        Validated clip length as integer
        
    Raises:
        ValueError: If clip length is invalid
    """
    try:
        length_int = int(length_bars)
        if length_int <= 0:
            raise ValueError("Clip length must be positive")
        return length_int
    except (ValueError, TypeError):
        raise ValueError(f"Invalid clip length: {length_bars}. Must be a positive integer.")


def validate_track_name(name: Any) -> str:
    """
    Validate track name.
    
    Args:
        name: Track name to validate
        
    Returns:
        Validated track name as string
        
    Raises:
        ValueError: If track name is invalid
    """
    if not name:
        raise ValueError("Track name cannot be empty")
    
    name_str = str(name).strip()
    if not name_str:
        raise ValueError("Track name cannot be empty or whitespace")
    
    if len(name_str) > 255:  # Reasonable limit
        raise ValueError("Track name cannot exceed 255 characters")
    
    return name_str