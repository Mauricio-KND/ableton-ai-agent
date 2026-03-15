#!/usr/bin/env python3
"""
Test different OSC address formats for AbletonOSC compatibility
"""

import sys
import os
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ableton_driver import AbletonDriver


def test_different_osc_formats():
    """Test different OSC address formats"""
    print("🧪 Testing Different OSC Address Formats")
    print("=" * 50)
    
    try:
        driver = AbletonDriver()
        
        # Different possible OSC address formats
        test_formats = [
            # Standard format
            ("/live/song/set/tempo", [125.0], "Standard format: /live/song/set/tempo"),
            
            # Alternative formats
            ("/live/tempo", [125.0], "Alternative: /live/tempo"),
            ("/tempo", [125.0], "Simple: /tempo"),
            ("/song/tempo", [125.0], "Song: /song/tempo"),
            
            # With different parameter formats
            ("/live/song/set/tempo", [125], "Integer parameter"),
            ("/live/song/set/tempo", [125.5], "Float parameter"),
            
            # Playback commands
            ("/live/song/start_playing", [], "Start playback"),
            ("/live/play", [], "Simple play"),
            ("/play", [], "Very simple play"),
            
            ("/live/song/stop_playing", [], "Stop playback"),
            ("/live/stop", [], "Simple stop"),
            ("/stop", [], "Very simple stop"),
        ]
        
        print("Testing different OSC address formats...")
        print("Watch Ableton Live for any changes in tempo or playback.")
        print("\nPress Enter after each test to continue...")
        
        for i, (command, args, description) in enumerate(test_formats):
            print(f"\n{i+1}. {description}")
            print(f"   Command: {command} {args}")
            
            try:
                driver.client.send_message(command, args)
                print("   ✅ Message sent")
                
                # Wait a moment to see if Ableton responds
                time.sleep(1.0)
                
                # For interactive testing
                if i < len(test_formats) - 1:
                    input("   Press Enter to continue to next test...")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print(f"\n🎯 Summary:")
        print(f"If any of the above commands caused changes in Ableton Live,")
        print(f"note which format worked and we can update the driver accordingly.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


def test_port_variations():
    """Test different port combinations"""
    print(f"\n🔌 Testing Different Port Combinations")
    print("=" * 50)
    
    port_combinations = [
        (11000, 11001, "Default: 11000/11001"),
        (8000, 9000, "Common: 8000/9000"),
        (9000, 8000, "Reversed: 9000/8000"),
        (12444, 12445, "Ableton default: 12444/12445"),
    ]
    
    for send_port, recv_port, description in port_combinations:
        print(f"\n{description}")
        print(f"   Send: {send_port}, Receive: {recv_port}")
        
        try:
            # Create temporary driver with different ports
            from pythonosc import udp_client
            client = udp_client.SimpleUDPClient("127.0.0.1", send_port)
            
            # Test tempo change
            client.send_message("/live/song/set/tempo", [128.0])
            print(f"   ✅ Tempo message sent to port {send_port}")
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")


def main():
    """Run all format tests"""
    print("🔍 AbletonOSC Format Compatibility Test")
    print("=" * 60)
    print("This test will help identify the correct OSC address format")
    print("and port combination for your AbletonOSC installation.")
    print("=" * 60)
    
    # Test different formats
    test_different_osc_formats()
    
    # Test port variations
    test_port_variations()
    
    print(f"\n📋 What to do next:")
    print(f"1. If any format worked - note the successful command")
    print(f"2. If nothing worked - check AbletonOSC documentation")
    print(f"3. Consider trying a different AbletonOSC version")
    print(f"4. Verify AbletonOSC is properly loaded in Ableton")


if __name__ == "__main__":
    main()