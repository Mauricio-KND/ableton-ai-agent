#!/usr/bin/env python3
"""
Discover what devices are available and how to work with them
"""

import sys
import os
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ableton_driver import AbletonDriver


def test_device_discovery():
    """Discover existing devices and available methods"""
    print("🔍 Device Discovery and Analysis")
    print("=" * 40)
    
    try:
        driver = AbletonDriver()
        
        # First, let's see what tracks exist and their devices
        print("1. Checking existing tracks and devices...")
        
        # Try to get track information
        track_commands = [
            ("/live/song/get/num_tracks", [], "Get number of tracks"),
            ("/live/song/get/track_names", [], "Get all track names"),
            ("/live/track/get/num_devices", [0], "Get devices on track 0"),
            ("/live/track/get/devices/name", [0], "Get device names on track 0"),
            ("/live/track/get/devices/class_name", [0], "Get device class names on track 0"),
        ]
        
        for command, args, description in track_commands:
            print(f"\n• {description}")
            print(f"  Command: {command} {args}")
            
            try:
                driver.client.send_message(command, args)
                print("  ✅ Query sent")
                time.sleep(1.0)
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        # Try to create a new track and then check devices
        print(f"\n2. Creating a test track and checking devices...")
        
        # Create a MIDI track
        driver.client.send_message("/live/song/create_midi_track", [0])
        time.sleep(2.0)
        
        # Check devices on the new track
        print("Checking devices on new track...")
        driver.client.send_message("/live/track/get/num_devices", [0])
        time.sleep(1.0)
        
        # Try to see if we can access the browser or device creation
        print(f"\n3. Testing browser and device access methods...")
        
        browser_commands = [
            ("/live/view/set/selected_track", [0], "Select track 0"),
            ("/live/browser/hotswap", [0], "Hotswap browser on track 0"),
            ("/live/browser/get/path", [], "Get browser path"),
            ("/live/browser/get/items", [], "Get browser items"),
        ]
        
        for command, args, description in browser_commands:
            print(f"\n• {description}")
            print(f"  Command: {command} {args}")
            
            try:
                driver.client.send_message(command, args)
                print("  ✅ Command sent")
                time.sleep(1.0)
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Discovery test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_alternative_device_methods():
    """Test alternative methods for device management"""
    print(f"\n🔄 Testing Alternative Device Methods")
    print("=" * 45)
    
    try:
        driver = AbletonDriver()
        
        # Try Live Object Model style commands
        lom_commands = [
            # Try to access device creation through LOM
            ("/live/song/get/track_data", [0, 1, "track.name", "track.devices.name"], "Get track and device data"),
            ("/live/track/get/clips/name", [0], "Get clip names (might trigger device info)"),
            
            # Try to see if there are any device-related commands we missed
            ("/live/test", [], "Test connection"),
            ("/live/application/get/version", [], "Get Ableton version"),
        ]
        
        for command, args, description in lom_commands:
            print(f"\n• {description}")
            print(f"  Command: {command} {args}")
            
            try:
                driver.client.send_message(command, args)
                print("  ✅ Command sent")
                time.sleep(1.0)
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Alternative methods test failed: {e}")
        return False


def main():
    """Run device discovery tests"""
    print("🚀 Device Discovery Suite")
    print("=" * 50)
    print("This test will help us understand what devices are available")
    print("and how we can work with them in AbletonOSC.")
    print("=" * 50)
    
    # Test device discovery
    test_device_discovery()
    
    # Test alternative methods
    test_alternative_device_methods()
    
    print(f"\n📋 Analysis:")
    print(f"1. Check the Ableton Live interface for any messages or responses")
    print(f"2. Look at the AbletonOSC logs for more detailed information")
    print(f"3. If device creation isn't supported, we may need to work with existing devices")
    print(f"4. Consider using MIDI clips with existing instruments instead")


if __name__ == "__main__":
    main()