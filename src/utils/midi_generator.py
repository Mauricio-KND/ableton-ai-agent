"""
MIDI generation utilities for the Ableton AI Agent

Provides functions for generating musical patterns, scales, and
chord progressions for automated music creation.
"""

from typing import List, Dict, Any, Tuple
import random


# Musical scales with their interval patterns
SCALES = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
    'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],
    'melodic_minor': [0, 2, 3, 5, 7, 9, 11],
    'dorian': [0, 2, 3, 5, 7, 9, 10],
    'phrygian': [0, 1, 3, 5, 7, 8, 10],
    'lydian': [0, 2, 4, 6, 7, 9, 11],
    'mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'locrian': [0, 1, 3, 5, 6, 8, 10],
    'pentatonic_major': [0, 2, 4, 7, 9],
    'pentatonic_minor': [0, 3, 5, 7, 10],
    'blues': [0, 3, 5, 6, 7, 10],
    'chromatic': list(range(12))
}

# Note names for MIDI conversion
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def note_to_midi(note_name: str) -> int:
    """
    Convert note name (e.g., "C4", "F#3") to MIDI note number.
    
    Args:
        note_name: Note name with octave
        
    Returns:
        MIDI note number (0-127)
        
    Raises:
        ValueError: If note name is invalid
    """
    # Extract note name and octave
    match = r'^([A-G]#?)(\d+)$'
    import re
    result = re.match(match, note_name.upper())
    if not result:
        raise ValueError(f"Invalid note name: {note_name}")
    
    note, octave = result.groups()
    octave = int(octave)
    
    # Find note index
    if note not in NOTE_NAMES:
        raise ValueError(f"Invalid note name: {note}")
    
    note_index = NOTE_NAMES.index(note)
    midi_note = (octave + 1) * 12 + note_index
    
    if not 0 <= midi_note <= 127:
        raise ValueError(f"Note {note_name} is out of MIDI range (0-127)")
    
    return midi_note


def midi_to_note(midi_note: int) -> str:
    """
    Convert MIDI note number to note name.
    
    Args:
        midi_note: MIDI note number (0-127)
        
    Returns:
        Note name with octave
    """
    if not 0 <= midi_note <= 127:
        raise ValueError("MIDI note must be between 0 and 127")
    
    note_index = midi_note % 12
    octave = (midi_note // 12) - 1
    return f"{NOTE_NAMES[note_index]}{octave}"


def generate_scale_notes(key: str, scale_type: str = 'major', octaves: int = 1) -> List[int]:
    """
    Generate MIDI notes for a specific scale.
    
    Args:
        key: Root note (e.g., "C", "F#")
        scale_type: Type of scale (major, minor, etc.)
        octaves: Number of octaves to generate
        
    Returns:
        List of MIDI note numbers
    """
    if scale_type not in SCALES:
        raise ValueError(f"Unknown scale type: {scale_type}")
    
    # Convert key to MIDI note
    root_note = note_to_midi(key + '3')  # Use octave 3 as base
    
    scale_intervals = SCALES[scale_type]
    notes = []
    
    for octave in range(octaves):
        for interval in scale_intervals:
            midi_note = root_note + (octave * 12) + interval
            if midi_note <= 127:  # Stay within MIDI range
                notes.append(midi_note)
    
    return notes


def generate_chord_progression(
    key: str, 
    progression: List[str], 
    scale_type: str = 'major'
) -> List[List[int]]:
    """
    Generate chord progressions based on scale degrees.
    
    Args:
        key: Root note
        progression: List of Roman numerals (e.g., ["I", "IV", "V", "I"])
        scale_type: Type of scale for chord generation
        
    Returns:
        List of chords, each chord is a list of MIDI notes
    """
    scale_notes = generate_scale_notes(key, scale_type, 2)
    
    # Roman numeral to scale degree mapping
    roman_to_degree = {
        'I': 0, 'II': 1, 'III': 2, 'IV': 3, 'V': 4, 'VI': 5, 'VII': 6,
        'i': 0, 'ii': 1, 'iii': 2, 'iv': 3, 'v': 4, 'vi': 5, 'vii': 6
    }
    
    chords = []
    
    for roman in progression:
        if roman.upper() not in roman_to_degree:
            raise ValueError(f"Invalid chord degree: {roman}")
        
        degree = roman_to_degree[roman]
        
        # Build triad (root, third, fifth)
        root = scale_notes[degree]
        third = scale_notes[(degree + 2) % len(scale_notes)]
        fifth = scale_notes[(degree + 4) % len(scale_notes)]
        
        # Adjust octave for notes that wrapped around
        if third < root:
            third += 12
        if fifth < root:
            fifth += 12
            
        chords.append([root, third, fifth])
    
    return chords


def generate_melody(
    key: str,
    scale_type: str = 'major',
    length_bars: int = 4,
    notes_per_bar: int = 4,
    rhythm_variety: float = 0.3
) -> List[Dict[str, Any]]:
    """
    Generate a simple melody using the specified scale.
    
    Args:
        key: Root note
        scale_type: Type of scale
        length_bars: Length in bars
        notes_per_bar: Average notes per bar
        rhythm_variety: Amount of rhythmic variation (0.0-1.0)
        
    Returns:
        List of MIDI note dictionaries
    """
    scale_notes = generate_scale_notes(key, scale_type, 2)
    melody = []
    
    total_notes = length_bars * notes_per_bar
    bar_duration = 4.0  # 4 beats per bar
    beat_duration = bar_duration / 4
    
    for i in range(total_notes):
        # Choose note from scale
        pitch = random.choice(scale_notes)
        
        # Calculate timing
        start_time = (i / notes_per_bar) * bar_duration
        
        # Add rhythmic variation
        if random.random() < rhythm_variety:
            duration = beat_duration * random.choice([0.5, 0.75, 1.0, 1.5])
        else:
            duration = beat_duration
        
        # Random velocity with musical preference
        velocity = random.randint(60, 100) if random.random() > 0.1 else random.randint(100, 127)
        
        melody.append({
            'pitch': pitch,
            'velocity': velocity,
            'start_time': start_time,
            'duration': duration
        })
    
    return melody


def generate_bassline(
    key: str,
    scale_type: str = 'major',
    length_bars: int = 4,
    pattern: str = 'simple'
) -> List[Dict[str, Any]]:
    """
    Generate a bassline pattern.
    
    Args:
        key: Root note
        scale_type: Type of scale
        length_bars: Length in bars
        pattern: Type of pattern ('simple', 'walking', 'arpeggiated')
        
    Returns:
        List of MIDI note dictionaries
    """
    scale_notes = generate_scale_notes(key, scale_type, 1)
    bassline = []
    
    bar_duration = 4.0
    beat_duration = bar_duration / 4
    
    if pattern == 'simple':
        # Root note on beat 1 and 3
        for bar in range(length_bars):
            for beat in [0, 2]:
                start_time = bar * bar_duration + beat * beat_duration
                bassline.append({
                    'pitch': scale_notes[0],  # Root note
                    'velocity': 80,
                    'start_time': start_time,
                    'duration': beat_duration * 2
                })
    
    elif pattern == 'walking':
        # Walking bassline using scale notes
        for bar in range(length_bars):
            for beat in range(4):
                start_time = bar * bar_duration + beat * beat_duration
                pitch = scale_notes[beat % len(scale_notes)]
                bassline.append({
                    'pitch': pitch,
                    'velocity': 70,
                    'start_time': start_time,
                    'duration': beat_duration * 0.9
                })
    
    elif pattern == 'arpeggiated':
        # Arpeggiated pattern
        chord_notes = scale_notes[:3]  # Use first 3 notes as chord
        for bar in range(length_bars):
            for i, pitch in enumerate(chord_notes):
                start_time = bar * bar_duration + i * beat_duration
                bassline.append({
                    'pitch': pitch,
                    'velocity': 75,
                    'start_time': start_time,
                    'duration': beat_duration
                })
    
    return bassline


def generate_drum_pattern(
    pattern_type: str = 'basic',
    length_bars: int = 4
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate drum patterns for different styles.
    
    Args:
        pattern_type: Type of drum pattern
        length_bars: Length in bars
        
    Returns:
        Dictionary with drum parts as MIDI notes
    """
    bar_duration = 4.0
    beat_duration = bar_duration / 4
    
    # MIDI notes for common drum sounds (General MIDI)
    KICK = 36
    SNARE = 38
    HI_HAT = 42
    OPEN_HAT = 46
    CRASH = 49
    
    drums = {'kick': [], 'snare': [], 'hihat': []}
    
    if pattern_type == 'basic':
        # Basic rock pattern
        for bar in range(length_bars):
            # Kick on 1 and 3
            for beat in [0, 2]:
                start_time = bar * bar_duration + beat * beat_duration
                drums['kick'].append({
                    'pitch': KICK,
                    'velocity': 100,
                    'start_time': start_time,
                    'duration': 0.1
                })
            
            # Snare on 2 and 4
            for beat in [1, 3]:
                start_time = bar * bar_duration + beat * beat_duration
                drums['snare'].append({
                    'pitch': SNARE,
                    'velocity': 90,
                    'start_time': start_time,
                    'duration': 0.1
                })
            
            # Hi-hats on all eighth notes
            for beat in range(8):
                start_time = bar * bar_duration + beat * beat_duration / 2
                drums['hihat'].append({
                    'pitch': HI_HAT,
                    'velocity': 60,
                    'start_time': start_time,
                    'duration': 0.05
                })
    
    elif pattern_type == 'four_on_floor':
        # Four-on-the-floor (techno/house)
        for bar in range(length_bars):
            for beat in range(4):
                start_time = bar * bar_duration + beat * beat_duration
                drums['kick'].append({
                    'pitch': KICK,
                    'velocity': 110,
                    'start_time': start_time,
                    'duration': 0.1
                })
            
            # Off-beat hi-hats
            for beat in range(8):
                if beat % 2 == 1:  # Off-beats
                    start_time = bar * bar_duration + beat * beat_duration / 2
                    drums['hihat'].append({
                        'pitch': HI_HAT,
                        'velocity': 70,
                        'start_time': start_time,
                        'duration': 0.05
                    })
    
    return drums


def generate_techno_pattern(
    key: str = 'E',
    scale_type: str = 'minor',
    length_bars: int = 4
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate a complete techno pattern with kick, bass, and lead.
    
    Args:
        key: Root key (default E minor for techno)
        scale_type: Scale type (minor for techno)
        length_bars: Length in bars
        
    Returns:
        Dictionary with all MIDI parts
    """
    patterns = {}
    
    # Techno kick - four-on-the-floor with some variation
    kick_pattern = []
    for bar in range(length_bars):
        for beat in range(4):
            start_time = bar * 4.0 + beat * 1.0
            velocity = 110 if beat in [0, 2] else 100  # Stronger on 1 and 3
            kick_pattern.append({
                'pitch': 36,  # C1 (kick)
                'velocity': velocity,
                'start_time': start_time,
                'duration': 0.1
            })
    patterns['kick'] = kick_pattern
    
    # Techno bassline - simple repetitive pattern
    bass_pattern = []
    scale_notes = generate_scale_notes(key, scale_type, 1)
    bass_notes = [scale_notes[0], scale_notes[3], scale_notes[0], scale_notes[5]]  # Root-5th pattern
    
    for bar in range(length_bars):
        for beat, note_idx in enumerate([0, 1, 0, 1]):  # Simple 2-note pattern
            start_time = bar * 4.0 + beat * 1.0
            if beat % 2 == 0:  # On kick beats
                bass_pattern.append({
                    'pitch': bass_notes[note_idx],
                    'velocity': 80,
                    'start_time': start_time,
                    'duration': 0.8
                })
    patterns['bass'] = bass_pattern
    
    # Techno lead - simple melodic pattern
    lead_pattern = []
    lead_notes = scale_notes[:5]  # Use pentatonic subset
    for bar in range(length_bars):
        for i in range(8):  # Eighth notes
            start_time = bar * 4.0 + i * 0.5
            if i % 4 == 0:  # Every other beat
                pitch = lead_notes[i % len(lead_notes)]
                lead_pattern.append({
                    'pitch': pitch + 12,  # Octave up
                    'velocity': 70,
                    'start_time': start_time,
                    'duration': 0.3
                })
    patterns['lead'] = lead_pattern
    
    # Hi-hats - 16th notes
    hihat_pattern = []
    for bar in range(length_bars):
        for i in range(16):
            start_time = bar * 4.0 + i * 0.25
            velocity = 50 if i % 2 == 0 else 40  # Accented pattern
            hihat_pattern.append({
                'pitch': 42,  # Closed hi-hat
                'velocity': velocity,
                'start_time': start_time,
                'duration': 0.05
            })
    patterns['hihat'] = hihat_pattern
    
    return patterns


def create_midi_clip_data(
    notes: List[Dict[str, Any]],
    clip_length: float = 4.0
) -> List[List]:
    """
    Convert note data to AbletonOSC MIDI format.
    
    Args:
        notes: List of note dictionaries
        clip_length: Length of the clip in bars
        
    Returns:
        List of MIDI note data for AbletonOSC
    """
    midi_data = []
    for note in notes:
        # AbletonOSC format: pitch, start_time, duration, velocity, mute
        midi_note = [
            note['pitch'],
            note['start_time'],
            note['duration'],
            note['velocity'],
            0  # mute (0 = unmuted)
        ]
        midi_data.append(midi_note)
    
    return midi_data
