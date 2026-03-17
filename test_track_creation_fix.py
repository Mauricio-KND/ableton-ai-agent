#!/usr/bin/env python3
"""
Test script to verify the track creation fix
"""

import sys
import os
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ableton_driver import AbletonDriver


def test_fixed_track_creation():
    """Test the corrected track creation methods"""
    print("🧪 Testing Fixed Track Creation")
    print("=" * 40)
    
    try:
        driver = AbletonDriver()
        
        print("Testing corrected track creation methods...")
        print("Watch Ableton Live for new tracks appearing.")
        print()
        
        # Test audio track creation
        print("1. Creating audio track at index 0...")
        driver.create_audio_track(0)
        time.sleep(2.0)
        
        # Test MIDI track creation  
        print("2. Creating MIDI track at index 1...")
        driver.create_midi_track(1)
        time.sleep(2.0)
        
        # Test creating tracks at end of list (-1)
        print("3. Creating audio track at end of list (-1)...")
        driver.create_audio_track(-1)
        time.sleep(2.0)
        
        print("4. Creating MIDI track at end of list (-1)...")
        driver.create_midi_track(-1)
        time.sleep(2.0)
        
        print()
        print("✅ Track creation test completed!")
        print("If you see new tracks in Ableton Live, the fix is working.")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Testing Track Creation Fix")
    print("=" * 50)
    print("This test verifies the corrected OSC addresses for track creation.")
    print("=" * 50)
    
    test_fixed_track_creation()