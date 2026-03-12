# Ableton AI Agent - Next Generation with MCP Integration

A robust, extensible AI agent for controlling Ableton Live through natural language commands. This system replaces the old OSC-based prototype with a comprehensive MCP (Model Context Protocol) architecture for enhanced reliability and functionality.

## 🎵 Overview

The Ableton AI Agent enables you to control Ableton Live using natural language commands like:
- "Create a techno track at 130 BPM"
- "Add reverb to the bass track"
- "Generate a schranz track at 169 BPM with a bassline and melody in F minor"
- "Set tempo to 140 BPM"
- "Start playback"

## 🏗️ Architecture

### Core Components

1. **MCP Tools System** - Modular tools for different Ableton functions
   - Track Management (`src/mcp_tools/track_tools.py`)
   - Session Control (`src/mcp_tools/session_tools.py`)
   - Clip Management (`src/mcp_tools/clip_tools.py`)
   - Device Management (`src/mcp_tools/device_tools.py`)

2. **State Management**
   - Memory Manager (`src/state/memory.py`) - Short-term memory for context
   - Session Manager (`src/state/session_manager.py`) - Real-time state tracking

3. **Utilities**
   - Logger (`src/utils/logger.py`) - Structured logging
   - Validators (`src/utils/validators.py`) - Input validation
   - MIDI Generator (`src/utils/midi_generator.py`) - Musical pattern generation

4. **Agent Core** (`src/agent.py`) - Main orchestration logic

## 🚀 Installation

### Prerequisites

- macOS (Apple Silicon M1/M2/M3 recommended)
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

### Step 2: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Mauricio-KND/ableton-ai-agent.git
cd ableton-ai-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
nano .env
```

Environment variables:
```env
OLLAMA_API_KEY=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
LOG_LEVEL=INFO
```

### Step 4: Setup Ableton Live

1. Open Ableton Live
2. Go to Preferences → Link MIDI
3. Ensure MIDI remote script is enabled
4. Set up MIDI ports if needed

## 🎮 Usage

### Basic Usage

```bash
# Run the agent
python -m src.agent

# Or directly
python src/agent.py
```

### Available Commands

#### Track Management
- `Create a [genre] track at [BPM] BPM`
- `Create MIDI track named "Drums"`
- `Delete track 2`
- `Set track volume to 0.7`
- `Mute track 1`
- `List all tracks`

#### Session Control
- `Set tempo to 140 BPM`
- `Start playback`
- `Stop playback`
- `Set time signature to 4/4`
- `Enable metronome`
- `Get session info`

#### Clip Management
- `Create MIDI clip in track 1`
- `Fire clip 2 in track 1`
- `Add MIDI notes to clip`
- `List clips in track 1`

#### Device Management
- `Add Reverb to track 1`
- `Add Operator synth to track 2`
- `Set device parameter`
- `List available devices`

#### Advanced Generation
- `Generate track: techno, 130, F minor, drums+bass+melody`

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

## 🔧 MCP Tools Reference

### Track Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `create_midi_track` | Create a new MIDI track | `name: str` |
| `create_audio_track` | Create a new audio track | `name: str` |
| `delete_track` | Delete a track | `track_id: int` |
| `set_track_name` | Rename a track | `track_id: int, name: str` |
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

## 🎼 Musical Features

### Supported Genres
- Techno
- House
- Schranz
- Trance
- Drum & Bass
- And more...

### Musical Elements
- **Drums**: Various patterns (four-on-floor, basic, etc.)
- **Bass**: Simple, walking, arpeggiated patterns
- **Melody**: Scale-based generation with rhythmic variety
- **Chords**: Diatonic progressions

### Supported Keys
- All major and minor keys
- Chromatic, pentatonic, blues scales
- Custom scale support

## 🔍 Logging and Debugging

The system provides comprehensive logging at multiple levels:

```bash
# Set log level in .env
LOG_LEVEL=DEBUG

# View logs in real-time
tail -f logs/ableton_agent.log
```

Log levels:
- `DEBUG`: Detailed execution information
- `INFO`: General operational information
- `WARNING`: Non-critical issues
- `ERROR`: Critical errors

## 🛠️ Development

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
├── ableton_driver.py      # Legacy Ableton driver
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

### Testing

```bash
# Run basic tests
python -m pytest tests/

# Test specific components
python -m pytest tests/test_track_tools.py

# Run with coverage
python -m pytest --cov=src tests/
```

## 🐛 Troubleshooting

### Common Issues

1. **Ollama Connection Failed**
   ```bash
   # Check if Ollama is running
   ollama list
   
   # Restart Ollama service
   ollama serve
   ```

2. **Ableton Not Responding**
   - Ensure Ableton Live is running
   - Check MIDI remote script settings
   - Verify MIDI ports are configured

3. **Model Not Found**
   ```bash
   # Pull the required model
   ollama pull llama3.2:3b
   ```

4. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   
   # Check Python version (3.8+ required)
   python --version
   ```

### Debug Mode

Enable debug logging for detailed troubleshooting:

```python
# In src/agent.py
agent = AbletonAgent(log_level="DEBUG")
```

## 🤝 Contributing

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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Ollama for providing the local LLM infrastructure
- Ableton for the Live API and remote script capabilities
- The MCP (Model Context Protocol) community for the architectural inspiration

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the logs for detailed error information

---

**🎵 Let's make some music with AI!**