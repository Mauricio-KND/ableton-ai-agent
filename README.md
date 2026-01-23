# Ableton Live AI Agent Controller
![CI Status](https://github.com/Mauricio-KND/ableton-ai-agent/actions/workflows/ci.yml/badge.svg)


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
1. Copy `.env.example` to `.env` and modify values as needed (this file should NOT be committed to version control)
2. For local development, you can set environment variables directly in your shell or use a .env file

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
