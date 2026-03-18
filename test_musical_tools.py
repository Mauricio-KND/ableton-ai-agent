#!/usr/bin/env python3
"""
Test script for the new musical tools functionality

This script tests the new musical generation capabilities including
techno patterns, basslines, melodies, and drum patterns.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent import AbletonAgent
from src.utils.midi_generator import (
    generate_techno_pattern, generate_bassline, generate_melody,
    generate_drum_pattern, create_midi_clip_data
)

def test_midi_generator():
    """Test the MIDI generator functions directly."""
    print("🎵 Testing MIDI Generator Functions")
    print("=" * 50)
    
    # Test techno pattern generation
    print("\n1. Testing Techno Pattern Generation:")
    try:
        techno_pattern = generate_techno_pattern('E', 'minor', 2)
        print(f"   ✅ Generated techno pattern with {len(techno_pattern)} parts")
        for part_name, notes in techno_pattern.items():
            print(f"      - {part_name}: {len(notes)} notes")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test bassline generation
    print("\n2. Testing Bassline Generation:")
    try:
        bassline = generate_bassline('C', 'minor', 2, 'simple')
        print(f"   ✅ Generated bassline with {len(bassline)} notes")
        # Show first few notes
        for i, note in enumerate(bassline[:3]):
            print(f"      - Note {i+1}: pitch={note['pitch']}, time={note['start_time']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test melody generation
    print("\n3. Testing Melody Generation:")
    try:
        melody = generate_melody('F', 'major', 2, 4, 0.3)
        print(f"   ✅ Generated melody with {len(melody)} notes")
        # Show first few notes
        for i, note in enumerate(melody[:3]):
            print(f"      - Note {i+1}: pitch={note['pitch']}, time={note['start_time']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test drum pattern generation
    print("\n4. Testing Drum Pattern Generation:")
    try:
        drums = generate_drum_pattern('four_on_floor', 2)
        print(f"   ✅ Generated drum pattern with {len(drums)} parts")
        for part_name, notes in drums.items():
            print(f"      - {part_name}: {len(notes)} notes")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test MIDI data conversion
    print("\n5. Testing MIDI Data Conversion:")
    try:
        test_notes = [
            {'pitch': 60, 'velocity': 100, 'start_time': 0.0, 'duration': 1.0},
            {'pitch': 64, 'velocity': 90, 'start_time': 1.0, 'duration': 0.5}
        ]
        midi_data = create_midi_clip_data(test_notes, 4.0)
        print(f"   ✅ Converted {len(test_notes)} notes to AbletonOSC format")
        for i, note in enumerate(midi_data):
            print(f"      - Note {i+1}: {note}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_musical_tools():
    """Test the musical tools through the agent."""
    print("\n\n🎛️  Testing Musical Tools via Agent")
    print("=" * 50)
    
    try:
        # Initialize agent
        agent = AbletonAgent()
        print("✅ Agent initialized successfully")
        
        # Test available tools
        musical_tools = [name for name in agent.available_tools.keys() if 'create_' in name and 'pattern' in name or 'bassline' in name or 'melody' in name or 'drum' in name]
        print(f"✅ Found {len(musical_tools)} musical tools: {musical_tools}")
        
        # Test techno pattern creation
        print("\n1. Testing Techno Pattern Tool:")
        result = agent.musical_tools.create_techno_pattern(
            kick_track_id=0,
            bass_track_id=1, 
            lead_track_id=2,
            key='E',
            scale_type='minor',
            length_bars=2
        )
        if result['success']:
            print(f"   ✅ {result['message']}")
            for part_name, part_result in result['parts'].items():
                print(f"      - {part_name}: {part_result.get('notes_count', 'N/A')} notes")
        else:
            print(f"   ❌ Error: {result.get('message', 'Unknown error')}")
        
        # Test bassline creation
        print("\n2. Testing Bassline Tool:")
        result = agent.musical_tools.create_bassline(
            track_id=0,
            key='C',
            scale_type='minor',
            length_bars=2,
            pattern_type='simple'
        )
        if result['success']:
            print(f"   ✅ {result['message']}")
        else:
            print(f"   ❌ Error: {result.get('message', 'Unknown error')}")
        
        # Test melody creation
        print("\n3. Testing Melody Tool:")
        result = agent.musical_tools.create_melody(
            track_id=1,
            key='F',
            scale_type='major',
            length_bars=2,
            notes_per_bar=4,
            rhythm_variety=0.3
        )
        if result['success']:
            print(f"   ✅ {result['message']}")
        else:
            print(f"   ❌ Error: {result.get('message', 'Unknown error')}")
        
        # Test drum pattern creation
        print("\n4. Testing Drum Pattern Tool:")
        result = agent.musical_tools.create_drum_pattern(
            track_id=2,
            pattern_type='four_on_floor',
            length_bars=2
        )
        if result['success']:
            print(f"   ✅ {result['message']}")
        else:
            print(f"   ❌ Error: {result.get('message', 'Unknown error')}")
        
        agent.shutdown()
        
    except Exception as e:
        print(f"❌ Error testing musical tools: {e}")

def test_natural_language_commands():
    """Test natural language commands that use musical tools."""
    print("\n\n🗣️  Testing Natural Language Commands")
    print("=" * 50)
    
    try:
        agent = AbletonAgent()
        
        test_commands = [
            "Create a techno pattern with kick, bass, and lead",
            "Add a bassline in E minor to track 0",
            "Create a melody in C major on track 1",
            "Generate a four-on-floor drum pattern on track 2"
        ]
        
        for i, command in enumerate(test_commands, 1):
            print(f"\n{i}. Testing: '{command}'")
            result = agent.execute(command)
            
            if result['success']:
                print(f"   ✅ {result['thought']}")
                print(f"   🔧 Executed {result['successful_commands']}/{result['total_commands']} commands")
                
                for cmd_result in result['results']:
                    if cmd_result['result']['success']:
                        print(f"      ✓ {cmd_result['result']['message']}")
                    else:
                        print(f"      ❌ {cmd_result['result']['message']}")
            else:
                print(f"   ❌ Error: {result.get('message', 'Unknown error')}")
        
        agent.shutdown()
        
    except Exception as e:
        print(f"❌ Error testing natural language commands: {e}")

def main():
    """Run all tests."""
    print("🧪 Ableton AI Agent - Musical Tools Test Suite")
    print("=" * 60)
    
    # Test MIDI generator functions
    test_midi_generator()
    
    # Test musical tools through agent
    test_musical_tools()
    
    # Test natural language commands
    test_natural_language_commands()
    
    print("\n\n🎉 Test Suite Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()