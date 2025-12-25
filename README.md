# My Desktop VTuber

A low-latency voice-based LLM interaction tool with Live2D avatar integration for hands-free AI conversations.

## Features

- **Real-time Voice Interaction** - Speak to your AI VTuber and hear responses with minimal latency
- **Live2D Avatar** - Animated character expressions responding to conversations
- **Multiple LLM Backends** - Support for OpenAI, Claude, Gemini, Ollama, and more
- **Offline Capable** - Core functionality works without internet connection
- **Cross-Platform** - Runs on Windows, macOS, and Linux

## Quick Start

### Two Interface Options

#### 🖥️ **Desktop Window Mode (Recommended for Standalone Use)**
The standalone desktop VTuber runs as a floating window overlay on your desktop. This mode is optimized for:
- **Hands-free AI interaction** - Talk directly to your avatar
- **Pet mode** - Avatar stays on screen while you work
- **No browser required** - True desktop application experience
- **Lower latency** - Direct system integration

**To use the Desktop VTuber:**
1. Download/build the project
2. Configure your LLM API keys in `conf.yaml`
3. Run: `uv run python run_server.py`
4. The desktop window will launch automatically
5. Start talking to your AI VTuber!

#### 🌐 **Web Interface Mode**
Access via browser at `http://localhost:12393` for:
- Cross-platform compatibility
- Easy sharing and collaboration
- Advanced configuration UI
- Works on any device with a browser

### Prerequisites
- Python 3.10 or higher
- FFmpeg for audio processing
- Git for submodule management (web mode)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/my-desktop-vtuber.git
cd my-desktop-vtuber

# Install dependencies using uv
uv sync

# Run the server
uv run python run_server.py
```

### Configuration

1. Edit `conf.yaml` with your API keys and preferences
2. Select your LLM backend (OpenAI, Claude, Gemini, etc.)
3. Choose a Live2D model from the available options
4. Run the server - desktop window will appear automatically

## Project Structure

```
src/open_llm_vtuber/      # Main application code
  ├── server.py           # FastAPI WebSocket server
  ├── config_manager/     # Configuration validation (Pydantic)
  ├── agent/              # LLM agent implementations
  ├── asr/                # Speech-to-text engines
  ├── tts/                # Text-to-speech engines
  ├── conversations/      # Conversation management
  └── mcpp/               # Model Context Protocol support

frontend/                 # Web UI (React app, git submodule)
live2d-models/           # Live2D model assets
config_templates/        # Configuration file templates
```

## Configuration

See `conf.yaml` for all available options:

- **LLM Backends** - OpenAI, Claude, Gemini, Ollama, and more
- **Voice Models** - Edge TTS, Azure Speech, Elevenlabs, etc.
- **Speech Recognition** - Faster Whisper, Azure ASR, Sherpa ONNX
- **Live2D Models** - Multiple avatar options

## Creating a Desktop Shortcut (Windows)

For easy access to the desktop VTuber, create a Windows shortcut:

1. **Right-click on Desktop** → New → Shortcut
2. **Enter this target path:**
   ```
   C:\Path\To\Your\Project\start_server.ps1
   ```
   (Replace with your actual project path)

3. **Name it:** "My Desktop VTuber"
4. **Right-click the shortcut** → Properties → Advanced → Check "Run as administrator"
5. **Double-click to launch!**

The VTuber window will open automatically with your configured avatar.

## Development

### Running in Development Mode

```bash
# With verbose logging
uv run python run_server.py --verbose

# Using Hugging Face mirror (faster in some regions)
uv run python run_server.py --hf_mirror
```

### Code Style

This project follows Python 3.10+ best practices with:
- Type hints for better IDE support
- Async/await for non-blocking operations
- Pydantic v2 for configuration validation
- Clean architecture with separation of concerns

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Nguyen Trung Kien** (kienntgch230116@fpt.edu.vn)

- Year Created: 2025
- Repository: https://github.com/yourusername/my-desktop-vtuber

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Uses [Pydantic](https://docs.pydantic.dev/) for configuration
- [Live2D](https://www.live2d.com/) for avatar framework
- Various LLM providers and open-source libraries
