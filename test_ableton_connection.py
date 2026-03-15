#!/usr/bin/env python3
"""
Test script to verify real Ableton Live communication
"""

import sys
import os
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ableton_driver import AbletonDriver
from src.config import Config


def test_ableton_connection():
    """Test direct communication with Ableton Live"""
    print("🧪 Testing Direct Ableton Live Communication")
    print("=" * 50)
    
    try:
        # Initialize AbletonDriver
        driver = AbletonDriver()
        print(f"✅ AbletonDriver initialized - sending to {Config.IP}:{Config.SEND_PORT}")
        
        # Test tempo change
        print("\n🎵 Testing tempo change...")
        print("   Setting tempo to 140 BPM...")
        driver.set_tempo(140.0)
        time.sleep(0.5)  # Wait for Ableton to process
        
        print("   Setting tempo to 120 BPM...")
        driver.set_tempo(120.0)
        time.sleep(0.5)
        
        # Test playback control
        print("\n▶️ Testing playback control...")
        print("   Starting playback...")
        driver.start_playback()
        time.sleep(2.0)  # Let it play for 2 seconds
        
        print("   Stopping playback...")
        driver.stop_playback()
        time.sleep(0.5)
        
        print("\n✅ All OSC messages sent successfully!")
        print("   Check Ableton Live to see if the tempo changed and playback started/stopped")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_with_agent():
    """Test through the agent interface"""
    print("\n🤖 Testing Through Agent Interface")
    print("=" * 50)
    
    try:
        from src.agent import AbletonAgent
        
        # Create agent
        agent = AbletonAgent()
        print("✅ Agent initialized")
        
        # Test tempo command
        print("\n🎵 Testing tempo command through agent...")
        result = agent.execute("Set tempo to 135 BPM")
        
        if result['success']:
            print("✅ Agent command executed successfully")
            print(f"   Thought: {result['thought']}")
            print(f"   Commands: {result['successful_commands']}/{result['total_commands']}")
            
            for cmd_result in result['results']:
                if cmd_result['result']['success']:
                    print(f"   ✓ {cmd_result['result']['message']}")
                else:
                    print(f"   ❌ {cmd_result['result']['message']}")
        else:
            print(f"❌ Agent command failed: {result.get('message', 'Unknown error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"\n❌ Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Ableton Live Connection Test Suite")
    print("=" * 60)
    print("Make sure:")
    print("1. Ableton Live is open")
    print("2. AbletonOSC control surface is configured with IAC Driver")
    print("3. IAC Driver is enabled in Audio MIDI Setup")
    print("=" * 60)
    
    # Test direct communication
    direct_success = test_ableton_connection()
    
    # Test through agent
    agent_success = test_with_agent()
    
    print("\n" + "=" * 60)
    if direct_success and agent_success:
        print("🎉 ALL TESTS PASSED!")
        print("\nThe agent is now communicating with Ableton Live!")
        print("You should see tempo changes and playback control in Ableton.")
    else:
        print("❌ Some tests failed.")
        if not direct_success:
            print("   - Direct OSC communication failed")
        if not agent_success:
            print("   - Agent communication failed")
        
        print("\nTroubleshooting:")
        print("1. Check that AbletonOSC is configured with IAC Driver")
        print("2. Verify Ableton Live is running")
        print("3. Check network/firewall settings")
        print("4. Ensure no other applications are using ports 11000/11001")


if __name__ == "__main__":
    main()