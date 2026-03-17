#!/usr/bin/env python3
"""
Research script to find the correct OSC commands for adding devices to tracks
"""

import sys
import os
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ableton_driver import AbletonDriver


def test_device_addition_commands():
    """Test different OSC commands for adding devices"""
    print("🧪 Testing Device Addition OSC Commands")
    print("=" * 50)
    
    try:
        driver = AbletonDriver()
        
        # Possible OSC address formats for device addition
        test_commands = [
            # Try different device addition patterns
            ("/live/device/add", [0, "Simpler"], "Add Simpler to track 0"),
            ("/live/device/add", [0, "Drift"], "Add Drift to track 0"),
            ("/live/device/add", [0, "Drum Rack"], "Add Drum Rack to track 0"),
            
            # Try with device type parameter
            ("/live/device/add", [0, "Simpler", "instrument"], "Add Simpler (instrument) to track 0"),
            ("/live/device/add", [0, "Drift", "instrument"], "Add Drift (instrument) to track 0"),
            ("/live/device/add", [0, "Drum Rack", "instrument"], "Add Drum Rack (instrument) to track 0"),
            
            # Try different address patterns
            ("/live/track/add_device", [0, "Simpler"], "Track add_device: Simpler"),
            ("/live/track/add_device", [0, "Drift"], "Track add_device: Drift"),
            ("/live/track/add_device", [0, "Drum Rack"], "Track add_device: Drum Rack"),
            
            # Try with device index
            ("/live/track/add_device", [0, "Simpler", 0], "Track add_device with index"),
            ("/live/track/add_device", [0, "Drift", 0], "Track add_device with index"),
            
            # Try Live Object Model style
            ("/live/view/set/selected_track", [0], "Select track 0 first"),
            ("/live/device/create", ["Simpler"], "Create device on selected track"),
            ("/live/device/create", ["Drift"], "Create device on selected track"),
            ("/live/device/create", ["Drum Rack"], "Create device on selected track"),
            
            # Try browser-based approach
            ("/live/browser/hotswap", [0], "Hotswap browser on track 0"),
            ("/live/browser/load", [0, "Simpler"], "Load device from browser"),
        ]
        
        print("Testing different OSC address formats for device addition...")
        print("Watch Ableton Live for new devices appearing on tracks.")
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
        print(f"If any of the above commands added devices to tracks in Ableton Live,")
        print(f"note which format worked and we can update the driver accordingly.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_device_query_commands():
    """Test commands to query existing devices"""
    print(f"\n🔍 Testing Device Query Commands")
    print("=" * 40)
    
    try:
        driver = AbletonDriver()
        
        # Test device query commands
        query_commands = [
            ("/live/track/get/devices/name", [0], "Get device names on track 0"),
            ("/live/track/get/num_devices", [0], "Get number of devices on track 0"),
            ("/live/track/get/devices/type", [0], "Get device types on track 0"),
            ("/live/device/get/name", [0, 0], "Get name of device 0 on track 0"),
            ("/live/device/get/class_name", [0, 0], "Get class name of device 0 on track 0"),
        ]
        
        print("Testing device query commands...")
        
        for command, args, description in query_commands:
            print(f"\n• {description}")
            print(f"  Command: {command} {args}")
            
            try:
                driver.client.send_message(command, args)
                print("  ✅ Query sent")
                time.sleep(1.0)
            except Exception as e:
                print(f"  ❌ Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Query test failed: {e}")
        return False


def main():
    """Run all device addition tests"""
    print("🚀 Device Addition Research Suite")
    print("=" * 60)
    print("This test will help identify the correct OSC address format")
    print("for adding devices to tracks in your AbletonOSC installation.")
    print("=" * 60)
    
    # Test device queries first
    test_device_query_commands()
    
    # Test device addition
    test_device_addition_commands()
    
    print(f"\n📋 What to do next:")
    print(f"1. If any format worked - note the successful command")
    print(f"2. If nothing worked - check AbletonOSC documentation for device creation")
    print(f"3. Try updating the AbletonDriver with the working format")
    print(f"4. Test the agent again with device addition commands")


if __name__ == "__main__":
    main()