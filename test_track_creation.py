#!/usr/bin/env python3
"""
Test script to verify track creation OSC commands
"""

import sys
import os
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ableton_driver import AbletonDriver
from src.config import Config


def test_track_creation_formats():
    """Test different OSC address formats for track creation"""
    print("🧪 Testing Track Creation OSC Commands")
    print("=" * 50)
    
    try:
        driver = AbletonDriver()
        
        # Different possible OSC address formats for track creation
        test_commands = [
            # Standard format (currently in AbletonDriver)
            ("/live/track/create", [0, "audio"], "Standard: /live/track/create [index, type]"),
            ("/live/track/create", [0, "midi"], "Standard: /live/track/create [index, type]"),
            
            # Alternative formats
            ("/live/track/create_audio", [0], "Alternative: /live/track/create_audio [index]"),
            ("/live/track/create_midi", [0], "Alternative: /live/track/create_midi [index]"),
            ("/live/create_track", [0, "audio"], "Simple: /live/create_track [index, type]"),
            ("/live/create/audio_track", [0], "Specific: /live/create/audio_track [index]"),
            ("/live/create/midi_track", [0], "Specific: /live/create/midi_track [index]"),
            
            # Without index parameter
            ("/live/track/create", ["audio"], "No index: /live/track/create [type]"),
            ("/live/track/create_audio", [], "No params: /live/track/create_audio"),
            ("/live/create_audio_track", [], "Simple no params: /live/create_audio_track"),
            
            # Different parameter order
            ("/live/track/create", ["audio", 0], "Swapped: /live/track/create [type, index]"),
        ]
        
        print("Testing different OSC address formats for track creation...")
        print("Watch Ableton Live for new tracks appearing.")
        print("\nPress Enter after each test to continue...")
        
        for i, (command, args, description) in enumerate(test_commands):
            print(f"\n{i+1}. {description}")
            print(f"   Command: {command} {args}")
            
            try:
                driver.client.send_message(command, args)
                print("   ✅ Message sent")
                
                # Wait a moment to see if Ableton responds
                time.sleep(2.0)
                
                # For interactive testing
                if i < len(test_commands) - 1:
                    input("   Press Enter to continue to next test...")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print(f"\n🎯 Summary:")
        print(f"If any of the above commands created tracks in Ableton Live,")
        print(f"note which format worked and we can update the driver accordingly.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_current_implementation():
    """Test the current AbletonDriver implementation"""
    print(f"\n🔧 Testing Current Implementation")
    print("=" * 50)
    
    try:
        driver = AbletonDriver()
        
        print("Testing current create_audio_track method...")
        driver.create_audio_track(0)
        time.sleep(2.0)
        
        print("Testing current create_midi_track method...")
        driver.create_midi_track(1)
        time.sleep(2.0)
        
        print("✅ Current implementation tested")
        print("Check if tracks appeared in Ableton Live")
        
        return True
        
    except Exception as e:
        print(f"❌ Current implementation test failed: {e}")
        return False


def main():
    """Run all track creation tests"""
    print("🚀 Track Creation OSC Test Suite")
    print("=" * 60)
    print("This test will help identify the correct OSC address format")
    print("for creating tracks in your AbletonOSC installation.")
    print("=" * 60)
    
    # Test current implementation first
    test_current_implementation()
    
    # Test different formats
    test_track_creation_formats()
    
    print(f"\n📋 What to do next:")
    print(f"1. If any format worked - note the successful command")
    print(f"2. If nothing worked - check AbletonOSC documentation")
    print(f"3. Try updating the AbletonDriver with the working format")
    print(f"4. Test the agent again with: 'Create a new audio track'")


if __name__ == "__main__":
    main()