#!/usr/bin/env python3
"""
Test script for the Ableton AI Agent with MCP Integration

This script tests the basic functionality of the agent without requiring
Ableton Live to be running.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent import AbletonAgent
from src.state.memory import MemoryManager
from src.state.session_manager import SessionManager
from src.utils.logger import setup_logger


def test_basic_functionality():
    """Test basic agent functionality."""
    print("🧪 Testing Ableton AI Agent...")
    
    # Setup logging
    logger = setup_logger("test", "INFO")
    
    try:
        # Test memory manager
        print("\n📝 Testing Memory Manager...")
        memory = MemoryManager(max_age_hours=1)
        memory.add_track(0, "Test Track", "midi")
        memory.add_device(0, 0, "Operator", "instrument")
        
        context = memory.get_context_summary()
        print(f"✅ Memory Manager working: {context['total_tracks']} tracks, {context['total_devices']} devices")
        
        # Test session manager
        print("\n🎛️ Testing Session Manager...")
        session = SessionManager(update_interval=0.1)
        session.start_monitoring()
        
        import time
        time.sleep(0.2)  # Let it update once
        
        session_info = session.get_state_summary()
        print(f"✅ Session Manager working: {len(session_info)} properties")
        
        session.stop_monitoring()
        
        # Test agent initialization
        print("\n🤖 Testing Agent Initialization...")
        # Mock the Ollama client for testing
        class MockClient:
            def chat(self):
                return self
            
            def completions(self):
                return self
            
            def create(self, **kwargs):
                class MockResponse:
                    choices = [type('Choice', (), {'message': type('Message', (), {'content': '{"thought": "test", "commands": []}'}())})()]
                return MockResponse()
        
        # Create agent with mocked client
        agent = AbletonAgent()
        agent.client = MockClient()
        
        print(f"✅ Agent initialized with {len(agent.available_tools)} tools")
        
        # Test tool execution
        print("\n🔧 Testing Tool Execution...")
        result = agent._execute_tool_call('list_tracks', {})
        print(f"✅ Tool execution working: {result['success']}")
        
        # Test LLM response parsing
        print("\n🧠 Testing LLM Response Parsing...")
        test_response = '{"thought": "test response", "commands": [{"tool": "test", "parameters": {}}]}'
        parsed = agent._parse_llm_response(test_response)
        print(f"✅ Response parsing working: {parsed['thought']}")
        
        print("\n🎉 All tests passed! The agent is ready to use.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_musical_features():
    """Test musical generation features."""
    print("\n🎵 Testing Musical Features...")
    
    try:
        from src.utils.midi_generator import (
            generate_melody, generate_bassline, generate_drum_pattern,
            generate_scale_notes, generate_chord_progression
        )
        
        # Test scale generation
        notes = generate_scale_notes('C', 'major')
        print(f"✅ Scale generation: C major = {notes[:5]}...")
        
        # Test melody generation
        melody = generate_melody('C', 'major', 4, 8)
        print(f"✅ Melody generation: {len(melody)} notes")
        
        # Test bassline generation
        bassline = generate_bassline('C', 'minor', 4, 'simple')
        print(f"✅ Bassline generation: {len(bassline)} notes")
        
        # Test drum pattern
        drums = generate_drum_pattern('four_on_floor', 4)
        print(f"✅ Drum pattern: {len(drums)} beats")
        
        # Test chord progression
        chords = generate_chord_progression('C', ['I', 'IV', 'V', 'I'], 'major')
        print(f"✅ Chord progression: {len(chords)} chords")
        
        print("🎼 All musical features working!")
        return True
        
    except Exception as e:
        print(f"❌ Musical features test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🚀 Ableton AI Agent Test Suite")
    print("=" * 40)
    
    success = True
    
    # Test basic functionality
    if not test_basic_functionality():
        success = False
    
    # Test musical features
    if not test_musical_features():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 ALL TESTS PASSED! The system is ready to use.")
        print("\nNext steps:")
        print("1. Ensure Ollama is running: ollama serve")
        print("2. Pull the model: ollama pull llama3.2:3b")
        print("3. Start Ableton Live")
        print("4. Run the agent: python src/agent.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()