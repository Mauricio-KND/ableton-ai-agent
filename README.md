# Ableton AI Agent

Control Ableton Live using natural language commands. This AI agent uses local LLM technology to understand your musical intentions and execute them directly in Ableton Live.

## What It Does

The Ableton AI Agent lets you:
- Create tracks and devices with simple commands
- Control session parameters like tempo and playback
- Generate musical patterns and arrangements
- Manage clips, tracks, and devices conversationally

Example commands:
- "Create a techno track at 130 BPM"
- "Add reverb to the bass track"
- "Set tempo to 140 BPM"
- "Start playback"
- "Generate a schranz track at 169 BPM with bassline and melody in F minor"

## Architecture

The system uses MCP (Model Context Protocol) architecture with these key components:

### Core System
- **MCP Tools**: Modular functions for different Ableton operations
- **State Management**: Memory system for context-aware operations
- **LLM Integration**: Local Ollama model for natural language processing
- **OSC Communication**: Direct communication with Ableton Live via AbletonOSC

### MCP Tools Categories
- **Track Management**: Create, delete, configure tracks
- **Session Control**: Tempo, playback, time signature
- **Clip Management**: Create, modify, launch clips
- **Device Management**: Add and control instruments/effects

## Installation

### System Requirements
- macOS (Apple Silicon recommended)
- Ableton Live 12 Lite or higher
- Python 3.8+
- Ollama with Llama 3.2 model

### Step 1: Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the required model
ollama pull llama3.2:3b

# Start Ollama service
ollama serve
```

### Step 2: Setup the Agent

```bash
# Clone the repository
git clone https://github.com/Mauricio-KND/ableton-ai-agent.git
cd ableton-ai-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env
```

### Step 3: Configure Ableton Live

1. Install AbletonOSC remote script in `/Music/Ableton/User Library/Remote Scripts`
2. Open Ableton Live Preferences → MIDI
3. Set Control Surface to "AbletonOSC"
4. Configure Input/Output
5. Enable Driver in Audio MIDI Setup

## Usage

### Start the Agent

```bash
# Run the agent
python -m src.agent
```

### Basic Commands

#### Track Operations
- "Create a techno track at 130 BPM"

#### Session Control
- "Set tempo to 140 BPM"
- "Start playback"
- "Stop playback"
- "Set time signature to 4/4"
- "Enable metronome"
- "Get session info"

#### Clip Management
- "Create MIDI clip in track 1"
- "Fire clip 2 in track 1"
- "Add MIDI notes to clip"
- "List clips in track 1"

#### Device Management
- "Add Reverb to track 1"
- "Add Operator synth to track 2"
- "Set device parameter"
- "List available devices"

#### Advanced Generation
- "Generate track: techno, 130, F minor, drums+bass+melody"

### Example Session

```
🎵 Ableton AI Agent with MCP Integration
Type 'help' for available commands or 'quit' to exit
==================================================

🎹 What would you like to do in Ableton? Create a techno track at 130 BPM

✅ Creating a techno track at 130 BPM by setting tempo and creating a MIDI track
🔧 Executed 2/2 commands
   ✓ Set tempo from 120.0 to 130.0
   ✓ Created MIDI track 'Techno Track' (ID 0) in track 0

🎹 What would you like to do in Ableton? Add Drum Rack to the techno track

✅ Finding the techno track and adding a Drum Rack device
🔧 Executed 1/1 commands
   ✓ Added instrument 'Drum Rack' (ID 0) to track 0

🎹 What would you like to do in Ableton? Start playback

✅ Starting playback
🔧 Executed 1/1 commands
   ✓ Started playback
```

## MCP Tools Reference

### Track Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| `create_midi_track` | Create new MIDI track | `name: str` |
| `create_audio_track` | Create new audio track | `name: str` |
| `delete_track` | Delete track | `track_id: int` |
| `set_track_name` | Rename track | `track_id: int, name: str` |
| `set_track_volume` | Set track volume | `track_id: int, volume: float (0.0-1.0)` |
| `set_track_mute` | Mute/unmute track | `track_id: int, mute: bool` |
| `get_track_info` | Get track information | `track_id: int` |
| `list_tracks` | List all tracks | `track_type: str (optional)` |

### Session Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| `set_tempo` | Set session tempo | `tempo: float (20-999)` |
| `get_tempo` | Get current tempo | - |
| `start_playback` | Start playback | - |
| `stop_playback` | Stop playback | - |
| `get_session_info` | Get session information | - |
| `save_session` | Save session | `name: str (optional)` |
| `set_time_signature` | Set time signature | `numerator: int, denominator: int` |
| `set_metronome` | Enable/disable metronome | `enabled: bool` |

### Clip Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| `create_midi_clip` | Create MIDI clip | `track_id: int, length_bars: int, name: str (optional)` |
| `delete_clip` | Delete clip | `track_id: int, clip_id: int` |
| `fire_clip` | Launch clip | `track_id: int, clip_id: int` |
| `stop_clip` | Stop clip | `track_id: int, clip_id: int` |
| `add_midi_notes` | Add MIDI notes | `track_id: int, clip_id: int, notes: list` |
| `clear_clip_notes` | Clear all notes | `track_id: int, clip_id: int` |
| `get_clip_info` | Get clip information | `track_id: int, clip_id: int` |
| `list_clips` | List clips | `track_id: int (optional)` |

### Device Tools
| Tool | Description | Parameters |
|------|-------------|------------|
| `add_device` | Add device to track | `track_id: int, device_name: str, device_type: str` |
| `remove_device` | Remove device | `track_id: int, device_id: int` |
| `set_device_parameter` | Set device parameter | `track_id: int, device_id: int, parameter_name: str, value: float` |
| `get_device_info` | Get device information | `track_id: int, device_id: int` |
| `list_devices` | List devices | `track_id: int (optional), device_type: str (optional)` |
| `list_available_devices` | List available devices | `device_type: str (optional)` |

## Musical Features

### Supported Genres
- Techno, House, Schranz, Trance, Drum & Bass, and more

### Musical Elements
- **Drums**: Various patterns (four-on-floor, basic, etc.)
- **Bass**: Simple, walking, arpeggiated patterns
- **Melody**: Scale-based generation with rhythmic variety
- **Chords**: Diatonic progressions

### Supported Keys
- All major and minor keys
- Chromatic, pentatonic, blues scales
- Custom scale support

## Troubleshooting

### Common Issues

**Ollama Connection Failed**
```bash
# Check if Ollama is running
ollama list

# Restart Ollama service
ollama serve
```

**Ableton Not Responding**
- Ensure Ableton Live is running
- Check AbletonOSC control surface settings
- Verify IAC Driver is configured correctly
- Confirm MIDI ports are set to "IAC Driver (Bus 1)"

**Model Not Found**
```bash
# Pull the required model
ollama pull llama3.2:3b
```

**Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python version (3.8+ required)
python --version
```

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
# Set log level in .env
LOG_LEVEL=DEBUG
```

## Development

### Project Structure

```
src/
├── agent.py                 # Main agent implementation
├── mcp_tools/              # MCP tool implementations
│   ├── track_tools.py      # Track management tools
│   ├── session_tools.py    # Session control tools
│   ├── clip_tools.py       # Clip management tools
│   └── device_tools.py     # Device management tools
├── state/                  # State management
│   ├── memory.py          # Short-term memory system
│   └── session_manager.py # Real-time session tracking
├── utils/                  # Utility functions
│   ├── logger.py          # Logging utilities
│   ├── validators.py      # Input validation
│   └── midi_generator.py  # Musical pattern generation
├── scanner.py             # Legacy Ableton scanner
├── ableton_driver.py      # Ableton OSC communication
└── config.py              # Configuration management
```

### Adding New Tools

1. Create a new tool file in `src/mcp_tools/`
2. Implement the tool class with `@mcp_tool` decorators
3. Initialize the tool in `src/agent.py`
4. Add tool to `_get_available_tools()` method

Example:
```python
@mcp_tool
def my_custom_tool(self, param1: str, param2: int) -> Dict[str, Any]:
    """Custom tool description."""
    try:
        # Implementation here
        return {
            'success': True,
            'message': f"Custom tool executed with {param1} and {param2}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f"Failed to execute custom tool: {e}"
        }
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Use type hints for all functions
- Add comprehensive docstrings
- Include error handling for all operations
- Write tests for new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the logs for detailed error information

---

Control Ableton Live with the power of AI.