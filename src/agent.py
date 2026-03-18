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
from .mcp_tools.musical_tools import initialize_musical_tools

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
        self.musical_tools = initialize_musical_tools(
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
        
        # Musical tools
        tools.update({
            'create_techno_pattern': self.musical_tools.create_techno_pattern,
            'create_bassline': self.musical_tools.create_bassline,
            'create_melody': self.musical_tools.create_melody,
            'create_drum_pattern': self.musical_tools.create_drum_pattern,
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

MUSICAL CONTENT CREATION WORKFLOW:
When users ask for musical patterns, basslines, melodies, or drums:
1. FIRST check if tracks already exist in memory context
2. Use existing track_ids (0, 1, 2, etc.) from memory
3. Use MUSICAL TOOLS for actual content creation:
   - create_bassline: For bass patterns
   - create_melody: For melodic content
   - create_drum_pattern: For drum patterns
   - create_techno_pattern: For complete techno arrangements
4. ONLY create new tracks if user specifically asks for new tracks

TRACK REFERENCE RULES:
1. Use track_ids (0, 1, 2) NOT track names for tool parameters
2. Check memory context for existing tracks before creating new ones
3. If user mentions "channel X" or "track X", find the corresponding track_id
4. NEVER create duplicate tracks - reuse existing ones when possible

MUSICAL TOOL EXAMPLES:
- "Create bass pattern" → use create_bassline with existing track_id
- "Add melody to track 1" → use create_melody with track_id=1
- "Make techno drums" → use create_drum_pattern or create_techno_pattern
- "Create bassline in E minor" → use create_bassline(key='E', scale_type='minor')

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

CRITICAL TRACK ID MANAGEMENT:
1. When creating tracks, the 'create_midi_track' and 'create_audio_track' tools return a 'track_id' (integer)
2. You MUST use these returned track_ids in subsequent commands that reference tracks
3. NEVER use placeholder names like '<Bass Track ID>' - always use the actual numeric track_id
4. Store track_ids mentally: track 0, track 1, track 2, etc.
5. Use track_ids for: set_track_volume, set_track_name, add_device, create_midi_clip, etc.

EXAMPLE WORKFLOWS:

Example 1 - Creating musical patterns on existing tracks:
User: "Create a bass midi pattern for the bass track and a lead pattern for the lead track"
Response: {{
  "thought": "Creating bass and lead patterns using existing tracks from memory",
  "commands": [
    {{"tool": "create_bassline", "parameters": {{"track_id": 0, "key": "E", "scale_type": "minor", "length_bars": 4}}}},
    {{"tool": "create_melody", "parameters": {{"track_id": 1, "key": "E", "scale_type": "minor", "length_bars": 4}}}}
  ]
}}

Example 2 - Complete techno song creation:
User: "Create a techno song with bass, lead, and drums"
Response: {{
  "thought": "Creating complete techno arrangement with tracks and musical content",
  "commands": [
    {{"tool": "set_tempo", "parameters": {{"tempo": 130}}}},
    {{"tool": "create_midi_track", "parameters": {{"name": "Bass"}}}},
    {{"tool": "create_midi_track", "parameters": {{"name": "Lead"}}}},
    {{"tool": "create_audio_track", "parameters": {{"name": "Drums"}}}},
    {{"tool": "create_techno_pattern", "parameters": {{"kick_track_id": 2, "bass_track_id": 0, "lead_track_id": 1, "key": "E", "scale_type": "minor", "length_bars": 4}}}}
  ]
}}

IMPORTANT GUIDELINES:
1. Always check memory context for existing tracks before creating new ones
2. Use MUSICAL TOOLS for content creation, not just empty clip creation
3. Use actual numeric track_ids (0, 1, 2, etc.) not placeholder names
4. For musical content, prefer create_bassline/create_melody over create_midi_clip
5. Break complex commands into logical sequences
6. Use descriptive names when creating new elements

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
        print("Ableton AI Agent with MCP Integration")
        print("Type 'help' for available commands or 'quit' to exit")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\nWhat would you like to do in Ableton? ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                    
                if user_input.lower() == 'help':
                    print("\nAvailable commands:")
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
                            print(f"\n{result['message']}")
                            for track_name in result['track_mapping'].values():
                                print(f"   Created: {track_name}")
                            continue
                    except (IndexError, ValueError):
                        print(f"Invalid generate command format. Use: 'generate track: genre, bpm, key, elements'")
                        continue
                
                # Execute regular command
                result = agent.execute(user_input)
                
                # Display results
                if result['success']:
                    print(f"\n{result['thought']}")
                    print(f"Executed {result['successful_commands']}/{result['total_commands']} commands")
                    
                    for cmd_result in result['results']:
                        if cmd_result['result']['success']:
                            print(f"   {cmd_result['result']['message']}")
                        else:
                            print(f"   {cmd_result['result']['message']}")
                else:
                    print(f"\nError: {result.get('message', 'Unknown error')}")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"\nUnexpected error: {e}")
                
    finally:
        agent.shutdown()


if __name__ == "__main__":
    main()