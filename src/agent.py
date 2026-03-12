"""
Next-generation Ableton AI Agent with MCP Integration

This agent replaces the old OSC-based system with a robust, extensible
MCP (Model Context Protocol) architecture for controlling Ableton Live.
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv

# Import new MCP-based components
from .state.memory import MemoryManager
from .state.session_manager import SessionManager
from .utils.logger import setup_logger, get_logger, LogContext
from .utils.validators import validate_tempo
from .utils.midi_generator import (
    generate_melody, generate_bassline, generate_drum_pattern
)

# Import MCP tools
from .mcp_tools.track_tools import initialize_track_tools
from .mcp_tools.session_tools import initialize_session_tools
from .mcp_tools.clip_tools import initialize_clip_tools
from .mcp_tools.device_tools import initialize_device_tools

# Legacy imports for backward compatibility
from .scanner import AbletonScanner
from .ableton_driver import AbletonDriver
from .config import Config

load_dotenv()


class AbletonAgent:
    """
    Next-generation Ableton AI Agent with MCP integration.
    
    This agent provides comprehensive control over Ableton Live through
    natural language commands, with robust error handling, state management,
    and extensible architecture.
    """
    
    def __init__(self, model_name: str = "llama3.2:3b", log_level: str = "INFO"):
        """Initialize the Ableton AI Agent."""
        self.logger = setup_logger("ableton_agent", log_level)
        self.logger.info("Initializing Ableton AI Agent with MCP architecture")
        
        # Initialize Ollama client
        self.client = OpenAI(
            api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        )
        self.model_name = model_name
        
        # Initialize core components
        self.memory_manager = MemoryManager(max_age_hours=2)
        self.session_manager = SessionManager(update_interval=1.0)
        
        # Initialize legacy components for backward compatibility
        self.scanner = AbletonScanner()
        self.driver = AbletonDriver()
        
        # Initialize MCP tools
        self.track_tools = initialize_track_tools(
            self.memory_manager, self.session_manager, self.driver
        )
        self.session_tools = initialize_session_tools(
            self.memory_manager, self.session_manager, self.driver
        )
        self.clip_tools = initialize_clip_tools(
            self.memory_manager, self.session_manager, self.driver
        )
        self.device_tools = initialize_device_tools(
            self.memory_manager, self.session_manager, self.driver
        )
        
        # Register available tools
        self.available_tools = self._get_available_tools()
        
        # Start session monitoring
        self.session_manager.start_monitoring()
        
        self.logger.info(f"Agent initialized with model: {model_name}")
        self.logger.info(f"Available tools: {len(self.available_tools)}")
        
    def _get_available_tools(self) -> Dict[str, Any]:
        """Get all available MCP tools."""
        tools = {}
        
        # Track tools
        tools.update({
            'create_midi_track': self.track_tools.create_midi_track,
            'create_audio_track': self.track_tools.create_audio_track,
            'delete_track': self.track_tools.delete_track,
            'set_track_name': self.track_tools.set_track_name,
            'set_track_volume': self.track_tools.set_track_volume,
            'set_track_mute': self.track_tools.set_track_mute,
            'get_track_info': self.track_tools.get_track_info,
            'list_tracks': self.track_tools.list_tracks,
        })
        
        # Session tools
        tools.update({
            'set_tempo': self.session_tools.set_tempo,
            'get_tempo': self.session_tools.get_tempo,
            'start_playback': self.session_tools.start_playback,
            'stop_playback': self.session_tools.stop_playback,
            'get_session_info': self.session_tools.get_session_info,
            'save_session': self.session_tools.save_session,
            'set_time_signature': self.session_tools.set_time_signature,
            'set_metronome': self.session_tools.set_metronome,
        })
        
        # Clip tools
        tools.update({
            'create_midi_clip': self.clip_tools.create_midi_clip,
            'delete_clip': self.clip_tools.delete_clip,
            'fire_clip': self.clip_tools.fire_clip,
            'stop_clip': self.clip_tools.stop_clip,
            'add_midi_notes': self.clip_tools.add_midi_notes,
            'clear_clip_notes': self.clip_tools.clear_clip_notes,
            'get_clip_info': self.clip_tools.get_clip_info,
            'list_clips': self.clip_tools.list_clips,
        })
        
        # Device tools
        tools.update({
            'add_device': self.device_tools.add_device,
            'remove_device': self.device_tools.remove_device,
            'set_device_parameter': self.device_tools.set_device_parameter,
            'get_device_info': self.device_tools.get_device_info,
            'list_devices': self.device_tools.list_devices,
            'list_available_devices': self.device_tools.list_available_devices,
        })
        
        return tools
        
    def _create_system_prompt(self, user_command: str) -> str:
        """Create a comprehensive system prompt for the LLM."""
        # Get current context
        session_info = self.session_tools.get_session_info()
        memory_context = self.memory_manager.get_context_summary()
        
        # Create tool descriptions
        tool_descriptions = []
        for tool_name, tool_func in self.available_tools.items():
            if hasattr(tool_func, '__doc__') and tool_func.__doc__:
                tool_descriptions.append(f"- {tool_name}: {tool_func.__doc__.strip()}")
        
        system_prompt = f"""
You are an expert Ableton Live controller with access to comprehensive MCP tools.
Your task is to understand natural language commands and convert them into precise tool calls.

CURRENT SESSION STATE:
{json.dumps(session_info.get('session_info', {}), indent=2)}

MEMORY CONTEXT (recently created elements):
{json.dumps(memory_context, indent=2)}

AVAILABLE TOOLS:
{chr(10).join(tool_descriptions)}

RESPONSE FORMAT:
You must respond with a JSON object containing:
{{
  "thought": "Brief explanation of your understanding and approach",
  "commands": [
    {{
      "tool": "tool_name",
      "parameters": {{"param1": "value1", "param2": "value2"}}
    }}
  ]
}}

IMPORTANT GUIDELINES:
1. Always check the current session state before making changes
2. Use memory context to reference previously created tracks/clips
3. Validate parameters before executing commands
4. Handle errors gracefully and provide helpful feedback
5. Break complex commands into multiple simple tool calls
6. Use descriptive names when creating new elements

EXAMPLES:
User: "Create a techno track at 130 BPM"
Response: {{
  "thought": "Creating a techno track at 130 BPM by setting tempo and creating a MIDI track",
  "commands": [
    {{"tool": "set_tempo", "parameters": {{"tempo": 130}}}},
    {{"tool": "create_midi_track", "parameters": {{"name": "Techno Track"}}}}
  ]
}}

Now process this command: "{user_command}"
"""
        return system_prompt
        
    def _execute_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single tool call with error handling."""
        if tool_name not in self.available_tools:
            return {
                'success': False,
                'error': f"Unknown tool: {tool_name}",
                'message': f"Tool '{tool_name}' is not available"
            }
        
        try:
            with LogContext(self.logger, f"Executing {tool_name}"):
                tool_func = self.available_tools[tool_name]
                result = tool_func(**parameters)
                
                if result.get('success', False):
                    self.logger.info(f"Tool {tool_name} executed successfully")
                else:
                    self.logger.warning(f"Tool {tool_name} failed: {result.get('message', 'Unknown error')}")
                
                return result
                
        except Exception as e:
            error_msg = f"Error executing {tool_name}: {str(e)}"
            self.logger.error(error_msg)
            return {
                'success': False,
                'error': str(e),
                'message': error_msg
            }
            
    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """Parse and validate the LLM response."""
        try:
            response = json.loads(response_text)
            
            # Validate response structure
            if not isinstance(response, dict):
                raise ValueError("Response must be a dictionary")
            
            if 'thought' not in response:
                response['thought'] = "No explanation provided"
            
            if 'commands' not in response:
                response['commands'] = []
            
            if not isinstance(response['commands'], list):
                raise ValueError("Commands must be a list")
            
            # Validate each command
            for i, cmd in enumerate(response['commands']):
                if not isinstance(cmd, dict):
                    raise ValueError(f"Command {i} must be a dictionary")
                
                if 'tool' not in cmd:
                    raise ValueError(f"Command {i} missing 'tool' field")
                
                if 'parameters' not in cmd:
                    cmd['parameters'] = {}
                
                if not isinstance(cmd['parameters'], dict):
                    raise ValueError(f"Command {i} parameters must be a dictionary")
            
            return response
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid response structure: {e}")
            
    def execute(self, user_command: str) -> Dict[str, Any]:
        """Execute a natural language command."""
        with LogContext(self.logger, f"Processing command: {user_command}"):
            try:
                # Create system prompt
                system_prompt = self._create_system_prompt(user_command)
                
                # Call LLM
                self.logger.info(f"Calling LLM with model: {self.model_name}")
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_command}
                    ],
                    response_format={'type': 'json_object'},
                    temperature=0.1
                )
                
                response_text = response.choices[0].message.content
                self.logger.info(f"LLM response received: {len(response_text)} characters")
                
                # Parse response
                parsed_response = self._parse_llm_response(response_text)
                
                # Execute commands
                results = []
                successful_commands = 0
                failed_commands = 0
                
                for i, command in enumerate(parsed_response['commands']):
                    self.logger.info(f"Executing command {i+1}/{len(parsed_response['commands'])}: {command['tool']}")
                    
                    result = self._execute_tool_call(command['tool'], command['parameters'])
                    results.append({
                        'command_index': i,
                        'tool': command['tool'],
                        'parameters': command['parameters'],
                        'result': result
                    })
                    
                    if result.get('success', False):
                        successful_commands += 1
                    else:
                        failed_commands += 1
                
                # Compile final result
                final_result = {
                    'success': failed_commands == 0,
                    'user_command': user_command,
                    'thought': parsed_response['thought'],
                    'total_commands': len(parsed_response['commands']),
                    'successful_commands': successful_commands,
                    'failed_commands': failed_commands,
                    'results': results,
                    'timestamp': datetime.now().isoformat()
                }
                
                if failed_commands == 0:
                    self.logger.info(f"Command executed successfully: {successful_commands} tools used")
                else:
                    self.logger.warning(f"Command partially executed: {successful_commands} successful, {failed_commands} failed")
                
                return final_result
                
            except Exception as e:
                error_msg = f"Failed to execute command: {str(e)}"
                self.logger.error(error_msg)
                return {
                    'success': False,
                    'error': str(e),
                    'message': error_msg,
                    'user_command': user_command,
                    'timestamp': datetime.now().isoformat()
                }
                
    def generate_track(self, genre: str, bpm: float, key: str, elements: List[str]) -> Dict[str, Any]:
        """High-level function to generate a complete track."""
        self.logger.info(f"Generating {genre} track at {bpm} BPM in {key}")
        
        # Set tempo
        self._execute_tool_call('set_tempo', {'tempo': bpm})
        
        # Create tracks based on elements
        track_mapping = {}
        for element in elements:
            if element in ['drums', 'percussion']:
                result = self._execute_tool_call('create_midi_track', {'name': f"{genre.title()} Drums"})
                if result.get('success'):
                    track_mapping['drums'] = result['name']
                    
            elif element in ['bass', 'bassline']:
                result = self._execute_tool_call('create_midi_track', {'name': f"{genre.title()} Bass"})
                if result.get('success'):
                    track_mapping['bass'] = result['name']
                    
            elif element in ['melody', 'lead', 'synth']:
                result = self._execute_tool_call('create_midi_track', {'name': f"{genre.title()} Lead"})
                if result.get('success'):
                    track_mapping['melody'] = result['name']
        
        return {
            'success': True,
            'genre': genre,
            'bpm': bpm,
            'key': key,
            'elements': elements,
            'track_mapping': track_mapping,
            'message': f"Generated {genre} track with {len(elements)} elements"
        }
        
    def shutdown(self):
        """Shutdown the agent and cleanup resources."""
        self.logger.info("Shutting down Ableton AI Agent")
        self.session_manager.stop_monitoring()
        self.logger.info("Agent shutdown complete")


def main():
    """Main function for command-line interface."""
    agent = AbletonAgent()
    
    try:
        print("🎵 Ableton AI Agent with MCP Integration")
        print("Type 'help' for available commands or 'quit' to exit")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n🎹 What would you like to do in Ableton? ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                    
                if user_input.lower() == 'help':
                    print("\n📖 Available commands:")
                    print("- 'Create a [genre] track at [BPM] BPM'")
                    print("- 'Add [device] to track [name/ID]'")
                    print("- 'Set tempo to [BPM]'")
                    print("- 'Start/Stop playback'")
                    print("- 'List tracks/devices/clips'")
                    print("- 'Generate track: [genre], [BPM], [key], [elements]'")
                    print("- 'Get session info'")
                    continue
                
                if not user_input:
                    continue
                
                # Check for high-level generate command
                if user_input.lower().startswith('generate track'):
                    try:
                        parts = user_input.split(':', 1)[1].strip()
                        elements = [p.strip() for p in parts.split(',')]
                        if len(elements) >= 4:
                            genre = elements[0]
                            bpm = float(elements[1])
                            key = elements[2]
                            track_elements = [e.strip() for e in elements[3].split('+')]
                            
                            result = agent.generate_track(genre, bpm, key, track_elements)
                            print(f"\n✅ {result['message']}")
                            for track_name in result['track_mapping'].values():
                                print(f"   🎵 Created: {track_name}")
                            continue
                    except (IndexError, ValueError):
                        print(f"❌ Invalid generate command format. Use: 'generate track: genre, bpm, key, elements'")
                        continue
                
                # Execute regular command
                result = agent.execute(user_input)
                
                # Display results
                if result['success']:
                    print(f"\n✅ {result['thought']}")
                    print(f"🔧 Executed {result['successful_commands']}/{result['total_commands']} commands")
                    
                    for cmd_result in result['results']:
                        if cmd_result['result']['success']:
                            print(f"   ✓ {cmd_result['result']['message']}")
                        else:
                            print(f"   ❌ {cmd_result['result']['message']}")
                else:
                    print(f"\n❌ Error: {result.get('message', 'Unknown error')}")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n💥 Unexpected error: {e}")
                
    finally:
        agent.shutdown()


if __name__ == "__main__":
    main()