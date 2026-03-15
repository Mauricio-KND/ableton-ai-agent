#!/usr/bin/env python3
"""
Integration test for the Ableton AI Agent
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent import AbletonAgent


def test_agent_with_mock():
    """Test agent with mocked LLM response"""
    print("🧪 Testing Agent Integration...")
    
    try:
        # Create agent
        agent = AbletonAgent()
        print(f"✅ Agent initialized with {len(agent.available_tools)} tools")
        
        # Mock the LLM client to return a test response
        class MockResponse:
            def __init__(self):
                self.choices = [type('Choice', (), {
                    'message': type('Message', (), {
                        'content': '{"thought": "Getting session information", "commands": [{"tool": "get_session_info", "parameters": {}}]}'
                    })()
                })()]
        
        def mock_create(**kwargs):
            return MockResponse()
        
        # Replace the client's create method
        agent.client.chat.completions.create = mock_create
        
        # Test command execution
        result = agent.execute("Get session info")
        
        if result['success']:
            print("✅ Command executed successfully")
            print(f"   Thought: {result['thought']}")
            print(f"   Commands: {result['total_commands']}")
            print(f"   Successful: {result['successful_commands']}")
        else:
            print(f"❌ Command failed: {result.get('message', 'Unknown error')}")
            
        return result['success']
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_real_ollama():
    """Test with real Ollama connection"""
    print("\n🌐 Testing Real Ollama Connection...")
    
    try:
        from openai import OpenAI
        
        # Test Ollama connection
        client = OpenAI(
            api_key="ollama",
            base_url="http://localhost:11434/v1",
        )
        
        # Simple test call
        response = client.chat.completions.create(
            model="llama3.2:3b",
            messages=[
                {"role": "user", "content": "Say 'Hello World'"}
            ],
            temperature=0.1
        )
        
        print(f"✅ Ollama connection working: {response.choices[0].message.content}")
        
        # Test with agent
        agent = AbletonAgent()
        result = agent.execute("Get session info")
        
        if result['success']:
            print("✅ Real agent execution successful")
            print(f"   Thought: {result['thought']}")
            return True
        else:
            print(f"❌ Real agent execution failed: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        return False


def main():
    """Run integration tests"""
    print("🚀 Ableton AI Agent Integration Tests")
    print("=" * 50)
    
    # Test with mock first
    mock_success = test_agent_with_mock()
    
    # Test with real Ollama
    real_success = test_real_ollama()
    
    print("\n" + "=" * 50)
    if mock_success and real_success:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("\nThe agent is ready to use with Ableton Live.")
        print("Run: python -m src.agent")
    else:
        print("❌ Some integration tests failed.")
        if not mock_success:
            print("   - Mock test failed (basic functionality)")
        if not real_success:
            print("   - Real Ollama test failed (check Ollama connection)")


if __name__ == "__main__":
    main()