# Ableton AI Agent (BETA)

MCP-based AI agent for controlling Ableton Live through natural language commands. Uses local LLM inference with enhanced musical pattern generation capabilities.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Input   │───▶│  LLM (Ollama)    │───▶│                  │
│  (Natural      │    │  llama3.2:3b     │    │      MCP Tools   │
│   Language)    │    │                  │    │                  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                       │
                       ┌──────────────────┐          │
                       │  State Manager   │◀─────────┘
                       │  (Memory +       │
                       │   Session)       │
                       └──────────────────┘
                                │
                       ┌──────────────────┐
                       │  Ableton Live    │
                       │  (via AbletonOSC)│
                       └──────────────────┘
```

### Core Components
- **MCP Tools**: Several modular functions for Ableton operations
- **LLM Integration**: Local Ollama
- **State Management**: Memory context and real-time session tracking
- **OSC Communication**: Direct Ableton Live control via AbletonOSC

## Quick Start

### Prerequisites
- macOS (Apple Silicon)
- Ableton Live 12 Lite+
- Python 3.8+
- Ollama

### Installation
```bash
# Clone and setup
git clone https://github.com/Mauricio-KND/ableton-ai-agent.git
cd ableton-ai-agent
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Setup Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:3b
ollama serve

# Configure Ableton Live
# 1. Install AbletonOSC in /Music/Ableton/User Library/Remote Scripts
# 2. Set Control Surface to "AbletonOSC" in Preferences → MIDI
```

### Run
```bash
python -m src.agent
```

### Verify Installation
```bash
python test_musical_tools.py  # Test musical pattern generation
```

## API Reference

### Track Management (Still testing)
| Tool | Function | Parameters |
|------|----------|------------|
| `create_midi_track` | Create MIDI track | `name: str` |
| `create_audio_track` | Create audio track | `name: str` |
| `delete_track` | Delete track | `track_id: int` |
| `set_track_name` | Rename track | `track_id: int, name: str` |
| `set_track_volume` | Set volume | `track_id: int, volume: float (0.0-1.0)` |
| `set_track_mute` | Mute/unmute | `track_id: int, mute: bool` |
| `get_track_info` | Track details | `track_id: int` |
| `list_tracks` | List tracks | `track_type: str (optional)` |

### Session Control (Still testing)
| Tool | Function | Parameters |
|------|----------|------------|
| `set_tempo` | Set BPM | `tempo: float (20-999)` |
| `get_tempo` | Get BPM | - |
| `start_playback` | Start playback | - |
| `stop_playback` | Stop playback | - |
| `get_session_info` | Session state | - |
| `save_session` | Save project | `name: str (optional)` |
| `set_time_signature` | Time signature | `numerator: int, denominator: int` |
| `set_metronome` | Metronome toggle | `enabled: bool` |

### Clip Management (Still testing)
| Tool | Function | Parameters |
|------|----------|------------|
| `create_midi_clip` | Create MIDI clip | `track_id: int, length_bars: int, name: str (optional)` |
| `delete_clip` | Delete clip | `track_id: int, clip_id: int` |
| `fire_clip` | Launch clip | `track_id: int, clip_id: int` |
| `stop_clip` | Stop clip | `track_id: int, clip_id: int` |
| `add_midi_notes` | Add notes | `track_id: int, clip_id: int, notes: list` |
| `clear_clip_notes` | Clear notes | `track_id: int, clip_id: int` |
| `get_clip_info` | Clip details | `track_id: int, clip_id: int` |
| `list_clips` | List clips | `track_id: int (optional)` |

### Device Management (Still testing)
| Tool | Function | Parameters |
|------|----------|------------|
| `add_device` | Add device | `track_id: int, device_name: str, device_type: str` |
| `remove_device` | Remove device | `track_id: int, device_id: int` |
| `set_device_parameter` | Set parameter | `track_id: int, device_id: int, parameter_name: str, value: float` |
| `get_device_info` | Device details | `track_id: int, device_id: int` |
| `list_devices` | List devices | `track_id: int (optional), device_type: str (optional)` |
| `list_available_devices` | Available devices | `device_type: str (optional)` |

### Musical Generation (Still testing)
| Tool | Function | Parameters |
|------|----------|------------|
| `create_techno_pattern` | Complete techno arrangement | `kick_track_id: int, bass_track_id: int, lead_track_id: int, key: str, scale_type: str, length_bars: int` |
| `create_bassline` | Bassline pattern | `track_id: int, key: str, scale_type: str, length_bars: int, pattern_type: str` |
| `create_melody` | Melody pattern | `track_id: int, key: str, scale_type: str, length_bars: int, notes_per_bar: int, rhythm_variety: float` |
| `create_drum_pattern` | Drum pattern | `track_id: int, pattern_type: str, length_bars: int` |

## Usage Examples

### Basic Operations
```python
# Track creation
agent.execute("Create a techno track at 130 BPM")

# Session control
agent.execute("Set tempo to 140 BPM")
agent.execute("Start playback")

# Device management
agent.execute("Add Reverb to track 1")
```

### Musical Pattern Generation
```python
# Complete patterns
agent.execute("Create a techno pattern with kick, bass, and lead")

# Individual elements
agent.execute("Create a bassline in E minor on track 0")
agent.execute("Add a melody in C major to track 1")
agent.execute("Generate four-on-floor drums on track 2")
```

### Advanced Workflows (Still testing)
```python
# Complete song generation
agent.execute("Generate track: techno, 130, F minor, drums+bass+melody")

# Context-aware operations
agent.execute("Add reverb to the bass track")  # Uses memory context
```

## Development

### Project Structure
```
src/
├── agent.py                 # Main agent with enhanced LLM guidance
├── mcp_tools/              # MCP tool implementations (34 tools)
│   ├── track_tools.py      # Track management (8 tools)
│   ├── session_tools.py    # Session control (8 tools)
│   ├── clip_tools.py       # Clip management (8 tools)
│   ├── device_tools.py     # Device management (6 tools)
│   └── musical_tools.py    # Musical generation (4 tools)
├── state/                  # State management
│   ├── memory.py          # Short-term memory with musical patterns
│   └── session_manager.py # Real-time session tracking
├── utils/                  # Core utilities
│   ├── logger.py          # Structured logging
│   ├── validators.py      # Input validation
│   └── midi_generator.py  # Musical pattern generation
├── ableton_driver.py      # OSC communication layer
└── config.py              # Configuration management
```

### Adding New Tools

1. **Create Tool Class**
```python
# src/mcp_tools/my_tools.py
class MyTools:
    @mcp_tool
    def my_tool(self, param: str) -> Dict[str, Any]:
        """Tool description for LLM."""
        try:
            # Implementation
            return {'success': True, 'message': 'Success'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
```

2. **Register Tool**
```python
# src/agent.py
def _get_available_tools(self):
    tools = {}
    tools.update({
        'my_tool': self.my_tools.my_tool,
    })
    return tools
```

### Testing Framework
```bash
# Core functionality
python test_complete_system.py

# Musical tools
python test_musical_tools.py

# Command processing
python test_musical_commands.py
```

## Configuration

### Environment Variables
```bash
# .env
OLLAMA_API_KEY=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
LOG_LEVEL=INFO
```

### Supported Musical Elements
- **Keys**: All major/minor, chromatic, pentatonic, blues
- **Patterns**: Four-on-floor, basic, walking, arpeggiated
- **Genres**: Techno, House, Trance, Drum & Bass
- **Rhythms**: Variable complexity (0.0-1.0 variety)

## Troubleshooting

### Common Issues
```bash
# Ollama connection
ollama list && ollama serve

# Ableton connection
# Check AbletonOSC control surface in Preferences → MIDI

# Python dependencies
pip install -r requirements.txt

# Debug mode
LOG_LEVEL=DEBUG python -m src.agent
```

### Performance Optimization
- Use your favorite model through Ollama
- Enable session monitoring for real-time updates
- Clear memory context periodically for long sessions

## Contributing

1. Fork repository
2. Create feature branch
3. Implement with type hints and error handling
4. Add tests for new tools
5. Update documentation
6. Submit PR

### Code Standards
- PEP 8 compliance
- Type hints required
- Comprehensive docstrings
- Error handling for all operations
- Test coverage for new features

## License

MIT License - see [LICENSE](LICENSE) file.

---

**Technical Architecture**: MCP-based system with tools and LLM guidance.