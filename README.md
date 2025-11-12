# J.A.R.V.I.S. - Voice Assistant for Mac

A local, privacy-focused voice assistant inspired by Iron Man's JARVIS. Built specifically for Mac M4 laptops, running entirely on your machine without requiring admin privileges.

## Features

- 🎤 **Wake Word Detection**: Say "Hey Jarvis" to activate
- 🗣️ **Speech Recognition**: Local speech-to-text using Faster-Whisper
- 🧠 **Local LLM**: Powered by Ollama (llama3.2:3b)
- 🛠️ **System Control**: Open apps, search files, control music, and more
- 💬 **Natural Conversation**: Context-aware responses
- 🖥️ **Futuristic GUI**: Terminal-style interface with animations
- 🔒 **Privacy First**: Everything runs locally on your Mac

## Demo

```
YOU: "Hey Jarvis"
JARVIS: [GUI opens]

YOU: "What's the time?"
JARVIS: "The current time is 3:42 PM, sir."

YOU: "Open Spotify"
JARVIS: "Opening Spotify, sir."

YOU: "Search for presentation files"
JARVIS: "Searching for presentation files. Found 5 files: ..."
```

## Prerequisites

### 1. Ollama

Install Ollama for local LLM:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Pull the model:

```bash
ollama pull llama3.2:3b
```

### 2. Picovoice API Key (Free)

For wake word detection:

1. Go to [console.picovoice.ai](https://console.picovoice.ai/)
2. Sign up for free account
3. Create an access key
4. Export it:

```bash
export PICOVOICE_API_KEY='your-key-here'
```

Add to your `~/.zshrc` or `~/.bash_profile` to persist:

```bash
echo 'export PICOVOICE_API_KEY="your-key-here"' >> ~/.zshrc
```

### 3. Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: First run will download the Whisper model (~140MB for base model).

## Installation

```bash
# Clone or download this project
cd ai-project

# Install dependencies
pip install -r requirements.txt

# Set up API key
export PICOVOICE_API_KEY='your-picovoice-key'

# Run Jarvis
python jarvis.py
```

## Configuration

Edit `config.yaml` to customize:

```yaml
wake_word: "jarvis"          # Wake word keyword
whisper_model: "base"        # STT model: tiny, base, small, medium
ollama_model: "llama3.2:3b"  # LLM model
voice: "Samantha"            # Mac voice (try: Alex, Daniel, Karen)
speech_rate: 200             # Words per minute

gui:
  background: "#000000"      # Black background
  text_color: "#00ff41"      # Matrix green
  width: 700
  height: 500
  transparency: 0.95         # Window transparency
```

## Usage

### Normal Mode (with Wake Word)

```bash
python jarvis.py
```

Say "Hey Jarvis" to activate. The GUI will open automatically.

### Test Mode (without Wake Word)

```bash
python jarvis.py --test
```

GUI opens immediately, and you can start speaking.

### Available Commands

**Open Applications:**
- "Open Chrome"
- "Launch Spotify"
- "Open Safari"

**Search Files:**
- "Find my presentation"
- "Search for Python files"

**Get Information:**
- "What's the time?"
- "What's the date?"
- "Check battery"
- "How much disk space?"

**Control Apps:**
- "Play music"
- "Pause"
- "Next track"
- "Volume up"

**Web Search:**
- "Search for Python tutorials"
- "Look up weather in New York"

**General Conversation:**
- "How are you?"
- "Tell me a joke"
- "What can you do?"

**Exit:**
- "Goodbye"
- "Exit"
- "Close"

## Troubleshooting

### Wake Word Not Working

1. Check API key is set:
   ```bash
   echo $PICOVOICE_API_KEY
   ```

2. Test microphone access:
   ```bash
   python -c "import sounddevice as sd; print(sd.query_devices())"
   ```

3. Grant Python microphone permission:
   - System Settings → Privacy & Security → Microphone
   - Enable for Terminal or Python

### Speech Recognition Not Working

1. Check Whisper model downloaded:
   ```bash
   ls ~/.cache/huggingface/hub/
   ```

2. Test manually:
   ```bash
   python -c "from modules.speech_to_text import SpeechToText; stt = SpeechToText(); print(stt.listen())"
   ```

### LLM Not Responding

1. Check Ollama is running:
   ```bash
   ollama list
   ```

2. Test model:
   ```bash
   ollama run llama3.2:3b "Hello"
   ```

3. If model not found:
   ```bash
   ollama pull llama3.2:3b
   ```

### GUI Not Showing

1. Check tkinter installation:
   ```bash
   python -c "import tkinter; print('OK')"
   ```

2. On macOS, tkinter comes with Python. If missing, reinstall Python from python.org

## Architecture

```
jarvis.py                 # Main orchestrator
├── modules/
│   ├── wake_word.py      # Porcupine wake word detection
│   ├── speech_to_text.py # Faster-Whisper STT
│   ├── llm_brain.py      # Ollama LLM with context
│   ├── text_to_speech.py # Mac 'say' command wrapper
│   ├── tools.py          # System automation tools
│   └── gui.py            # Tkinter futuristic interface
├── prompts/
│   └── system_prompt.txt # LLM instructions for tool use
└── config.yaml           # Configuration
```

## Performance Tips

- **Faster STT**: Use `whisper_model: "tiny"` (less accurate but faster)
- **Better Accuracy**: Use `whisper_model: "small"` or `"medium"`
- **Smaller LLM**: Use `llama3.2:1b` for faster responses
- **Better Responses**: Use `llama3.2` (full version, ~4GB)

## Known Limitations

- **No Admin Access**: Cannot control system settings or install software
- **Mac Only**: Uses Mac-specific commands (`say`, `open`, `osascript`)
- **English Only**: STT configured for English (can be changed in code)
- **Local Only**: No cloud integration (this is a feature!)

## Customization

### Change Wake Word

Available options: jarvis, alexa, computer, hey google, hey siri, jarvis, ok google, picovoice, porcupine, terminator

Edit `config.yaml`:
```yaml
wake_word: "computer"
```

### Change Voice

List available voices:
```bash
say -v "?"
```

Popular choices:
- `Samantha` - Female, friendly
- `Alex` - Male, clear
- `Daniel` - Male, British
- `Karen` - Female, Australian

### Change GUI Theme

Edit `config.yaml`:
```yaml
gui:
  background: "#0a0a0a"    # Dark grey
  text_color: "#00aaff"    # Blue
```

### Add Custom Tools

Edit `modules/tools.py` and add your tool handler:

```python
def _my_custom_tool(self, data: Dict[str, Any]) -> tuple[bool, str]:
    """My custom tool."""
    # Your implementation
    return True, "Success message"
```

Add to `tool_handlers` dict and update `prompts/system_prompt.txt`.

## Future Enhancements

- [ ] Web-based UI with more sophisticated animations
- [ ] Integration with Mac Shortcuts app
- [ ] Persistent memory across sessions
- [ ] Multi-language support
- [ ] Custom wake word training
- [ ] Home automation integration
- [ ] Calendar and reminders
- [ ] Email and messaging

## Contributing

Feel free to fork and customize for your needs!

## License

MIT License - Use freely, no warranty provided.

## Credits

Built with:
- [Ollama](https://ollama.com/) - Local LLM
- [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) - Speech recognition
- [Picovoice Porcupine](https://picovoice.ai/) - Wake word detection
- [Python](https://python.org/) - Programming language

Inspired by Marvel's JARVIS from Iron Man.

---

**Made with ⚡ for Mac M4**

