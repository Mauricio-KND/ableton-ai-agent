# Ableton Live AI Agent Controller

Control Ableton Live using natural language commands via local AI (Ollama) and OSC protocol.

## Features
- Natural language processing for music production commands
- Real-time control of tracks, clips, and effects
- macOS integration with local Ollama LLM
- OSC communication with Ableton Live

## Requirements
- macOS (optimized for Apple Silicon)
- Python 3.10+
- Ableton Live 11+ with OSC enabled
- Ollama running locally (no API key required)

## Installation
```bash
git clone https://github.com/Mauricio-KND/ableton-ai-agent.git
cd ableton-ai-agent
pip install -r requirements.txt
```

## Configuration
1. Create `.env` file in project root:
```ini
# Ollama configuration (legacy variable names preserved)
DEEPSEEK_API_KEY=ollama  # No actual key needed for local Ollama
DEEPSEEK_BASE_URL=http://localhost:11431/v1

# Ableton OSC settings
ABLETON_IP=127.0.0.1
ABLETON_SEND_PORT=11000
ABLETON_RECEIVE_PORT=11001
DEBUG_MODE=True
```

## Usage
```python
from src.agent import AbletonAgent

agent = AbletonAgent()
agent.execute("Create a schranz-style bass in F minor")
```

## Project Structure
```
├── src/
│   ├── config.py       # Connection configuration
│   ├── agent.py        # Core AI agent logic
│   ├── scanner.py      # Ableton state monitoring
│   └── ableton_driver.py # OSC communication handler
├── data/               # Session snapshots
└── tests/              # Integration tests
```

## Example Commands
- "Add techno kick drum to track 3"
- "Increase reverb wetness by 30% on channel 2"
- "Launch clip 5 in main track with 4-bar loop"
