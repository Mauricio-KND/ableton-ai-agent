#!/usr/bin/env python3
"""
Diagnose AbletonOSC configuration and communication
"""

import sys
import os
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ableton_driver import AbletonDriver
from src.config import Config


def diagnose_osc_communication():
    """Diagnose OSC communication issues"""
    print("🔍 AbletonOSC Communication Diagnosis")
    print("=" * 50)
    
    print(f"📡 Configuration:")
    print(f"   IP: {Config.IP}")
    print(f"   Send Port: {Config.SEND_PORT}")
    print(f"   Receive Port: {Config.RECEIVE_PORT}")
    
    print(f"\n🧪 Testing OSC Message Sending...")
    
    try:
        driver = AbletonDriver()
        
        # Test different OSC commands that AbletonOSC should understand
        test_commands = [
            ("/live/song/set/tempo", [130.0], "Set tempo to 130 BPM"),
            ("/live/song/start_playing", [], "Start playback"),
            ("/live/song/stop_playing", [], "Stop playback"),
            ("/live/song/get/tempo", [], "Get current tempo"),
            ("/live/song/get/num_tracks", [], "Get number of tracks"),
        ]
        
        for command, args, description in test_commands:
            print(f"\n   📤 Sending: {description}")
            print(f"      Command: {command} {args}")
            driver.client.send_message(command, args)
            time.sleep(0.2)
        
        print(f"\n✅ All OSC messages sent!")
        print(f"\n❓ Did you see any changes in Ableton Live?")
        print(f"   - Tempo should have changed to 130 BPM")
        print(f"   - Playback should have started and stopped")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error sending OSC messages: {e}")
        return False


def check_abletonosc_requirements():
    """Check AbletonOSC requirements"""
    print(f"\n📋 AbletonOSC Configuration Checklist:")
    print(f"=" * 50)
    
    requirements = [
        "✅ Ableton Live is running",
        "❓ AbletonOSC remote script is installed in: ~/Music/Ableton/User Library/Remote Scripts",
        "❓ Control Surface is set to 'AbletonOSC' in Ableton Preferences",
        "❓ Input/Output ports are set to 'IAC Driver (Bus 1)'",
        "❓ IAC Driver is enabled in Audio MIDI Setup",
        "❓ No firewall blocking UDP ports 11000/11001",
    ]
    
    for req in requirements:
        print(f"   {req}")
    
    print(f"\n🔧 Common Issues:")
    print(f"   1. Wrong OSC address format - some AbletonOSC versions use different paths")
    print(f"   2. Port mismatch - AbletonOSC might use different ports")
    print(f"   3. MIDI vs UDP - some versions use MIDI instead of UDP")
    print(f"   4. AbletonOSC version compatibility")


def suggest_alternatives():
    """Suggest alternative approaches"""
    print(f"\n💡 Alternative Approaches:")
    print(f"=" * 30)
    
    print(f"1. Check AbletonOSC documentation for correct OSC addresses")
    print(f"2. Try different port combinations (8000/9000, 9000/8000)")
    print(f"3. Use MIDI messages instead of OSC if AbletonOSC supports it")
    print(f"4. Test with a simple OSC client like TouchOSC or OSCulator")
    print(f"5. Check AbletonOSC log files for error messages")


def main():
    """Run diagnosis"""
    diagnose_osc_communication()
    check_abletonosc_requirements()
    suggest_alternatives()
    
    print(f"\n🎯 Next Steps:")
    print(f"1. If you saw changes in Ableton Live - the OSC communication is working!")
    print(f"2. If no changes occurred - check the AbletonOSC configuration")
    print(f"3. Try the agent command again: 'python -m src.agent'")
    print(f"4. Test with: 'set tempo to 140 bpm'")


if __name__ == "__main__":
    main()