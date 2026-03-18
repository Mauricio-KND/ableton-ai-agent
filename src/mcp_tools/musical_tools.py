"""
Musical generation MCP tools for Ableton Live control

Provides tools for generating complete musical patterns, including
techno patterns, basslines, melodies, and drum patterns with actual
MIDI content that can be added to clips.
"""

from typing import Dict, Any, List, Optional
import functools

from ..utils.logger import get_logger
from ..utils.validators import validate_track_id, validate_tempo
from ..utils.midi_generator import (
    generate_techno_pattern, generate_bassline, generate_melody,
    generate_drum_pattern, create_midi_clip_data
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


class MusicalTools:
    """
    Collection of MCP tools for musical content generation.
    
    This class provides tools for creating complete musical patterns
    with actual MIDI content that can be added to Ableton Live clips.
    """
    
    def __init__(
        self, 
        memory_manager: MemoryManager,
        session_manager: SessionManager,
        ableton_client: Any = None
    ):
        """
        Initialize musical tools.
        
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
    def create_techno_pattern(
        self, 
        kick_track_id: int,
        bass_track_id: int,
        lead_track_id: int,
        key: str = 'E',
        scale_type: str = 'minor',
        length_bars: int = 4
    ) -> Dict[str, Any]:
        """
        Create a complete techno pattern with kick, bass, lead, and hi-hats.
        USE THIS for creating full techno arrangements with actual MIDI content.
        
        Args:
            kick_track_id: Track ID for kick drum (must be existing track)
            bass_track_id: Track ID for bassline (must be existing track)
            lead_track_id: Track ID for lead synth (must be existing track)
            key: Root key for the pattern (e.g., 'E', 'C', 'F')
            scale_type: Scale type ('minor', 'major', 'dorian', etc.)
            length_bars: Length of the pattern in bars (typically 4 or 8)
            
        Returns:
            Dictionary containing pattern creation result with note counts
            
        Example:
            create_techno_pattern(kick_track_id=2, bass_track_id=0, lead_track_id=1, key='E', scale_type='minor', length_bars=4)
        """
        try:
            # Validate track IDs
            kick_track_id = validate_track_id(kick_track_id)
            bass_track_id = validate_track_id(bass_track_id)
            lead_track_id = validate_track_id(lead_track_id)
            
            self.logger.info(f"Creating techno pattern in {key} {scale_type} for {length_bars} bars")
            
            # Generate techno pattern
            pattern = generate_techno_pattern(key, scale_type, length_bars)
            
            results = {}
            
            # Create clips and add MIDI data for each part
            if self.ableton:
                # Create kick clip
                kick_clip_result = self._create_clip_with_midi(
                    kick_track_id, pattern['kick'], f"Techno Kick", length_bars
                )
                results['kick'] = kick_clip_result
                
                # Create bass clip
                bass_clip_result = self._create_clip_with_midi(
                    bass_track_id, pattern['bass'], f"Techno Bass", length_bars
                )
                results['bass'] = bass_clip_result
                
                # Create lead clip
                lead_clip_result = self._create_clip_with_midi(
                    lead_track_id, pattern['lead'], f"Techno Lead", length_bars
                )
                results['lead'] = lead_clip_result
                
                # Create hi-hat clip (optional - could use same track as kick or separate)
                if len(pattern['hihat']) > 0:
                    hihat_clip_result = self._create_clip_with_midi(
                        kick_track_id, pattern['hihat'], f"Techno Hi-Hats", length_bars
                    )
                    results['hihat'] = hihat_clip_result
            else:
                # Simulate clip creation
                for part_name, notes in pattern.items():
                    results[part_name] = {
                        'success': True,
                        'clip_id': len(self.session.clips),
                        'notes_count': len(notes),
                        'message': f"Created {part_name} clip with {len(notes)} notes"
                    }
            
            # Update memory
            self.memory.add_musical_pattern(
                f"techno_{key}_{scale_type}", 
                [kick_track_id, bass_track_id, lead_track_id],
                pattern
            )
            
            self.logger.info(f"Successfully created techno pattern with {len(results)} parts")
            
            return {
                'success': True,
                'pattern_type': 'techno',
                'key': key,
                'scale_type': scale_type,
                'length_bars': length_bars,
                'parts': results,
                'message': f"Created techno pattern in {key} {scale_type} with {len(results)} parts"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create techno pattern: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create techno pattern: {e}"
            }
    
    @mcp_tool
    def create_bassline(
        self,
        track_id: int,
        key: str = 'C',
        scale_type: str = 'minor',
        length_bars: int = 4,
        pattern_type: str = 'simple'
    ) -> Dict[str, Any]:
        """
        Create a bassline pattern with actual MIDI notes and add it to a track.
        USE THIS for creating bass content instead of empty clips.
        
        Args:
            track_id: Track ID to add bassline to (must be existing track)
            key: Root key for the bassline (e.g., 'E', 'C', 'F')
            scale_type: Scale type ('minor', 'major', 'dorian', etc.)
            length_bars: Length in bars (typically 4 or 8)
            pattern_type: Type of bassline pattern ('simple', 'walking', 'arpeggiated')
            
        Returns:
            Dictionary containing bassline creation result with note count
            
        Example:
            create_bassline(track_id=0, key='E', scale_type='minor', length_bars=4, pattern_type='simple')
        """
        try:
            track_id = validate_track_id(track_id)
            
            self.logger.info(f"Creating {pattern_type} bassline in {key} {scale_type}")
            
            # Generate bassline
            bassline = generate_bassline(key, scale_type, length_bars, pattern_type)
            
            # Create clip and add MIDI data
            if self.ableton:
                clip_result = self._create_clip_with_midi(
                    track_id, bassline, f"Bassline ({pattern_type})", length_bars
                )
            else:
                clip_result = {
                    'success': True,
                    'clip_id': len(self.session.clips),
                    'notes_count': len(bassline),
                    'message': f"Created bassline clip with {len(bassline)} notes"
                }
            
            # Update memory
            self.memory.add_musical_pattern(
                f"bassline_{pattern_type}", [track_id], {'bassline': bassline}
            )
            
            self.logger.info(f"Successfully created {pattern_type} bassline with {len(bassline)} notes")
            
            return {
                'success': True,
                'track_id': track_id,
                'key': key,
                'scale_type': scale_type,
                'pattern_type': pattern_type,
                'length_bars': length_bars,
                'notes_count': len(bassline),
                'clip_result': clip_result,
                'message': f"Created {pattern_type} bassline with {len(bassline)} notes"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create bassline: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create bassline: {e}"
            }
    
    @mcp_tool
    def create_melody(
        self,
        track_id: int,
        key: str = 'C',
        scale_type: str = 'major',
        length_bars: int = 4,
        notes_per_bar: int = 4,
        rhythm_variety: float = 0.3
    ) -> Dict[str, Any]:
        """
        Create a melody with actual MIDI notes and add it to a track.
        USE THIS for creating melodic content instead of empty clips.
        
        Args:
            track_id: Track ID to add melody to (must be existing track)
            key: Root key for the melody (e.g., 'E', 'C', 'F')
            scale_type: Scale type ('minor', 'major', 'dorian', etc.)
            length_bars: Length in bars (typically 4 or 8)
            notes_per_bar: Average notes per bar (2-8 recommended)
            rhythm_variety: Amount of rhythmic variation (0.0-1.0)
            
        Returns:
            Dictionary containing melody creation result with note count
            
        Example:
            create_melody(track_id=1, key='E', scale_type='minor', length_bars=4, notes_per_bar=4, rhythm_variety=0.3)
        """
        try:
            track_id = validate_track_id(track_id)
            
            self.logger.info(f"Creating melody in {key} {scale_type}")
            
            # Generate melody
            melody = generate_melody(key, scale_type, length_bars, notes_per_bar, rhythm_variety)
            
            # Create clip and add MIDI data
            if self.ableton:
                clip_result = self._create_clip_with_midi(
                    track_id, melody, f"Melody", length_bars
                )
            else:
                clip_result = {
                    'success': True,
                    'clip_id': len(self.session.clips),
                    'notes_count': len(melody),
                    'message': f"Created melody clip with {len(melody)} notes"
                }
            
            # Update memory
            self.memory.add_musical_pattern(
                f"melody_{key}_{scale_type}", [track_id], {'melody': melody}
            )
            
            self.logger.info(f"Successfully created melody with {len(melody)} notes")
            
            return {
                'success': True,
                'track_id': track_id,
                'key': key,
                'scale_type': scale_type,
                'length_bars': length_bars,
                'notes_count': len(melody),
                'clip_result': clip_result,
                'message': f"Created melody with {len(melody)} notes"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create melody: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create melody: {e}"
            }
    
    @mcp_tool
    def create_drum_pattern(
        self,
        track_id: int,
        pattern_type: str = 'four_on_floor',
        length_bars: int = 4
    ) -> Dict[str, Any]:
        """
        Create a drum pattern with actual MIDI notes and add it to a track.
        USE THIS for creating drum content instead of empty clips.
        
        Args:
            track_id: Track ID to add drum pattern to (must be existing track)
            pattern_type: Type of drum pattern ('basic', 'four_on_floor')
            length_bars: Length in bars (typically 4 or 8)
            
        Returns:
            Dictionary containing drum pattern creation result with note count
            
        Example:
            create_drum_pattern(track_id=2, pattern_type='four_on_floor', length_bars=4)
        """
        try:
            track_id = validate_track_id(track_id)
            
            self.logger.info(f"Creating {pattern_type} drum pattern")
            
            # Generate drum pattern
            drums = generate_drum_pattern(pattern_type, length_bars)
            
            # Combine all drum parts into one pattern
            all_notes = []
            for part_name, notes in drums.items():
                all_notes.extend(notes)
            
            # Sort by start time
            all_notes.sort(key=lambda x: x['start_time'])
            
            # Create clip and add MIDI data
            if self.ableton:
                clip_result = self._create_clip_with_midi(
                    track_id, all_notes, f"Drums ({pattern_type})", length_bars
                )
            else:
                clip_result = {
                    'success': True,
                    'clip_id': len(self.session.clips),
                    'notes_count': len(all_notes),
                    'message': f"Created drum pattern clip with {len(all_notes)} notes"
                }
            
            # Update memory
            self.memory.add_musical_pattern(
                f"drums_{pattern_type}", [track_id], {'drums': drums}
            )
            
            self.logger.info(f"Successfully created {pattern_type} drum pattern with {len(all_notes)} notes")
            
            return {
                'success': True,
                'track_id': track_id,
                'pattern_type': pattern_type,
                'length_bars': length_bars,
                'notes_count': len(all_notes),
                'parts': list(drums.keys()),
                'clip_result': clip_result,
                'message': f"Created {pattern_type} drum pattern with {len(all_notes)} notes"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create drum pattern: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create drum pattern: {e}"
            }
    
    def _create_clip_with_midi(
        self,
        track_id: int,
        notes: List[Dict[str, Any]],
        clip_name: str,
        length_bars: int
    ) -> Dict[str, Any]:
        """
        Helper method to create a clip and add MIDI notes.
        
        Args:
            track_id: Track ID to create clip on
            notes: List of MIDI note dictionaries
            clip_name: Name for the clip
            length_bars: Length of the clip in bars
            
        Returns:
            Dictionary containing clip creation result
        """
        try:
            # Create clip
            clip_length = length_bars * 4.0  # Convert bars to beats
            self.ableton.client.send_message("/live/clip_slot/create_clip", [track_id, 0, clip_length])
            
            # Convert notes to AbletonOSC format
            midi_data = create_midi_clip_data(notes, clip_length)
            
            # Add notes to clip
            for midi_note in midi_data:
                self.ableton.client.send_message("/live/clip/add/notes", [track_id, 0] + midi_note)
            
            return {
                'success': True,
                'track_id': track_id,
                'clip_id': 0,
                'notes_count': len(notes),
                'length_bars': length_bars,
                'message': f"Created clip '{clip_name}' with {len(notes)} notes"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create clip with MIDI: {e}"
            }


# Global instance for MCP tool registration
_musical_tools_instance: Optional[MusicalTools] = None


def initialize_musical_tools(
    memory_manager: MemoryManager,
    session_manager: SessionManager,
    ableton_client: Any = None
) -> MusicalTools:
    """
    Initialize the musical tools with required dependencies.
    
    Args:
        memory_manager: Memory manager instance
        session_manager: Session manager instance
        ableton_client: Ableton client instance
        
    Returns:
        Initialized MusicalTools instance
    """
    global _musical_tools_instance
    _musical_tools_instance = MusicalTools(memory_manager, session_manager, ableton_client)
    return _musical_tools_instance


def get_musical_tools() -> Optional[MusicalTools]:
    """Get the global musical tools instance."""
    return _musical_tools_instance


# Export individual tool functions for MCP registration
def create_techno_pattern(
    kick_track_id: int,
    bass_track_id: int,
    lead_track_id: int,
    key: str = 'E',
    scale_type: str = 'minor',
    length_bars: int = 4
) -> Dict[str, Any]:
    """Create a complete techno pattern."""
    if not _musical_tools_instance:
        raise RuntimeError("Musical tools not initialized")
    return _musical_tools_instance.create_techno_pattern(
        kick_track_id, bass_track_id, lead_track_id, key, scale_type, length_bars
    )


def create_bassline(
    track_id: int,
    key: str = 'C',
    scale_type: str = 'minor',
    length_bars: int = 4,
    pattern_type: str = 'simple'
) -> Dict[str, Any]:
    """Create a bassline pattern."""
    if not _musical_tools_instance:
        raise RuntimeError("Musical tools not initialized")
    return _musical_tools_instance.create_bassline(
        track_id, key, scale_type, length_bars, pattern_type
    )


def create_melody(
    track_id: int,
    key: str = 'C',
    scale_type: str = 'major',
    length_bars: int = 4,
    notes_per_bar: int = 4,
    rhythm_variety: float = 0.3
) -> Dict[str, Any]:
    """Create a melody."""
    if not _musical_tools_instance:
        raise RuntimeError("Musical tools not initialized")
    return _musical_tools_instance.create_melody(
        track_id, key, scale_type, length_bars, notes_per_bar, rhythm_variety
    )


def create_drum_pattern(
    track_id: int,
    pattern_type: str = 'four_on_floor',
    length_bars: int = 4
) -> Dict[str, Any]:
    """Create a drum pattern."""
    if not _musical_tools_instance:
        raise RuntimeError("Musical tools not initialized")
    return _musical_tools_instance.create_drum_pattern(
        track_id, pattern_type, length_bars
    )