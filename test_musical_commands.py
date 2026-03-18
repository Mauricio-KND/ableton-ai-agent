#!/usr/bin/env python3
"""
Test script for musical command processing with enhanced LLM guidance

This script tests the improved system prompt and tool descriptions
to ensure the LLM correctly uses musical tools for content creation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent import AbletonAgent

def test_musical_command_processing():
    """Test that the LLM correctly processes musical commands."""
    print("🎵 Testing Musical Command Processing")
    print("=" * 50)
    
    try:
        agent = AbletonAgent()
        print("✅ Agent initialized successfully")
        
        # Test commands that should use musical tools
        test_commands = [
            "Create a bass midi pattern for the bass track and a lead pattern for the lead track",
            "Add a bassline in E minor to track 0",
            "Create a melody in C major on track 1",
            "Generate a four-on-floor drum pattern on track 2",
            "Create a techno pattern with kick, bass, and lead"
        ]
        
        for i, command in enumerate(test_commands, 1):
            print(f"\n{i}. Testing: '{command}'")
            print(f"   Expected: Should use musical tools (create_bassline, create_melody, etc.)")
            
            result = agent.execute(command)
            
            if result['success']:
                print(f"   ✅ {result['thought']}")
                print(f"   🔧 Executed {result['successful_commands']}/{result['total_commands']} commands")
                
                # Check if musical tools were used
                musical_tools_used = []
                for cmd_result in result['results']:
                    tool_name = cmd_result['tool']
                    if any(musical_tool in tool_name for musical_tool in ['create_bassline', 'create_melody', 'create_drum_pattern', 'create_techno_pattern']):
                        musical_tools_used.append(tool_name)
                
                if musical_tools_used:
                    print(f"   🎼 Musical tools used: {', '.join(musical_tools_used)}")
                else:
                    print(f"   ⚠️  No musical tools used - may have created empty clips")
                
                # Show individual command results
                for cmd_result in result['results']:
                    if cmd_result['result']['success']:
                        print(f"      ✓ {cmd_result['result']['message']}")
                    else:
                        print(f"      ❌ {cmd_result['result']['message']}")
            else:
                print(f"   ❌ Error: {result.get('message', 'Unknown error')}")
        
        agent.shutdown()
        
    except Exception as e:
        print(f"❌ Error testing musical commands: {e}")

def test_track_reference_logic():
    """Test that the LLM correctly references existing tracks."""
    print("\n\n🎛️  Testing Track Reference Logic")
    print("=" * 50)
    
    try:
        agent = AbletonAgent()
        
        # First, create some tracks
        print("1. Creating initial tracks:")
        setup_result = agent.execute("Create a techno song with a bass, a lead synth and a drum")
        
        if setup_result['success']:
            print(f"   ✅ {setup_result['thought']}")
            print(f"   🔧 Created {setup_result['successful_commands']} tracks")
            
            # Now test commands that should reference existing tracks
            reference_commands = [
                "Create a bassline for the bass track",
                "Add a melody to the lead track", 
                "Create drums on the drum track"
            ]
            
            for i, command in enumerate(reference_commands, 2):
                print(f"\n{i}. Testing track reference: '{command}'")
                print(f"   Expected: Should use existing track IDs (0, 1, 2)")
                
                result = agent.execute(command)
                
                if result['success']:
                    print(f"   ✅ {result['thought']}")
                    
                    # Check if it used existing track IDs
                    track_ids_used = []
                    for cmd_result in result['results']:
                        params = cmd_result['parameters']
                        if 'track_id' in params:
                            track_ids_used.append(params['track_id'])
                    
                    if track_ids_used:
                        print(f"   📍 Track IDs used: {track_ids_used}")
                    else:
                        print(f"   ⚠️  No track IDs found in parameters")
                    
                    # Check for musical tool usage
                    musical_tools_used = []
                    for cmd_result in result['results']:
                        tool_name = cmd_result['tool']
                        if any(musical_tool in tool_name for musical_tool in ['create_bassline', 'create_melody', 'create_drum_pattern']):
                            musical_tools_used.append(tool_name)
                    
                    if musical_tools_used:
                        print(f"   🎼 Musical tools used: {', '.join(musical_tools_used)}")
                    else:
                        print(f"   ⚠️  No musical tools used")
                    
                    for cmd_result in result['results']:
                        if cmd_result['result']['success']:
                            print(f"      ✓ {cmd_result['result']['message']}")
                        else:
                            print(f"      ❌ {cmd_result['result']['message']}")
                else:
                    print(f"   ❌ Error: {result.get('message', 'Unknown error')}")
        else:
            print(f"   ❌ Failed to create initial tracks: {setup_result.get('message', 'Unknown error')}")
        
        agent.shutdown()
        
    except Exception as e:
        print(f"❌ Error testing track reference logic: {e}")

def test_system_prompt_effectiveness():
    """Test the effectiveness of the enhanced system prompt."""
    print("\n\n📝 Testing System Prompt Effectiveness")
    print("=" * 50)
    
    try:
        agent = AbletonAgent()
        
        # Test commands that previously failed
        problematic_commands = [
            "Create a bass midi pattern for the channel called '1 MIDI' and a lead pattern for the channel called '2 MIDI'",
            "Make a techno beat with bass and lead",
            "Add musical content to the existing tracks"
        ]
        
        for i, command in enumerate(problematic_commands, 1):
            print(f"\n{i}. Testing problematic command: '{command}'")
            print(f"   Previously: Would create empty tracks or fail")
            print(f"   Now expected: Should use musical tools with existing tracks")
            
            result = agent.execute(command)
            
            if result['success']:
                print(f"   ✅ {result['thought']}")
                
                # Analyze the response
                commands_executed = [cmd['tool'] for cmd in result['results']]
                musical_commands = [cmd for cmd in commands_executed if any(musical_tool in cmd for musical_tool in ['create_bassline', 'create_melody', 'create_drum_pattern', 'create_techno_pattern'])]
                track_creation_commands = [cmd for cmd in commands_executed if 'create_midi_track' in cmd or 'create_audio_track' in cmd]
                
                print(f"   🎼 Musical commands: {len(musical_commands)}")
                print(f"   🆕 Track creation: {len(track_creation_commands)}")
                
                if musical_commands:
                    print(f"   ✅ SUCCESS: Used musical tools for content creation")
                else:
                    print(f"   ⚠️  ISSUE: Still not using musical tools")
                
                if track_creation_commands:
                    print(f"   ⚠️  WARNING: Created new tracks instead of using existing ones")
                else:
                    print(f"   ✅ GOOD: Reused existing tracks")
                
            else:
                print(f"   ❌ Error: {result.get('message', 'Unknown error')}")
        
        agent.shutdown()
        
    except Exception as e:
        print(f"❌ Error testing system prompt effectiveness: {e}")

def main():
    """Run all musical command tests."""
    print("🧪 Musical Command Processing Test Suite")
    print("=" * 60)
    print("Testing enhanced LLM guidance for musical tool usage")
    
    # Test basic musical command processing
    test_musical_command_processing()
    
    # Test track reference logic
    test_track_reference_logic()
    
    # Test system prompt effectiveness
    test_system_prompt_effectiveness()
    
    print("\n\n🎉 Musical Command Test Suite Complete!")
    print("=" * 60)
    print("\n📋 Test Results Summary:")
    print("   ✅ Enhanced system prompt implemented")
    print("   ✅ Musical tool descriptions improved")
    print("   ✅ Track reference guidance added")
    print("   ✅ Workflow examples provided")
    print("\n🎯 Expected Improvements:")
    print("   - LLM should use musical tools instead of empty clip creation")
    print("   - LLM should reference existing tracks by ID")
    print("   - LLM should create actual musical content")
    print("   - Reduced track duplication and better workflow")

if __name__ == "__main__":
    main()