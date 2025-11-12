# JARVIS Quick Reference

## Setup Commands

```bash
# One-line setup
./setup.sh

# Or manually:
ollama pull llama3.2:3b
pip3 install -r requirements.txt
export PICOVOICE_API_KEY='your-key'
```

## Running JARVIS

```bash
python3 jarvis.py              # With wake word
python3 jarvis.py --test       # Without wake word (GUI opens immediately)
python3 test_components.py     # Test individual components
```

## Common Commands

### System
- "What's the time?"
- "What's the date?"
- "Check battery"
- "How much disk space?"

### Applications
- "Open [app name]" (Chrome, Safari, Spotify, etc.)
- "Launch [app name]"

### Files
- "Search for [filename]"
- "Find [keyword] files"

### Music Control (for Music app/Spotify)
- "Play music"
- "Pause"
- "Next track"
- "Previous track"
- "Volume up/down"

### Web
- "Search for [query]"
- "Look up [topic]"

### Conversation
- "How are you?"
- "What can you do?"
- "Tell me about yourself"

### Exit
- "Goodbye"
- "Exit"
- "Close"

## Configuration Quick Edits

### Change Voice
Edit `config.yaml`:
```yaml
voice: "Samantha"  # Try: Alex, Daniel, Karen, Victoria
```

List all voices:
```bash
say -v "?"
```

### Change GUI Colors
Edit `config.yaml`:
```yaml
gui:
  text_color: "#00ff41"  # Matrix green
  # Try: "#00aaff" (blue), "#ff00ff" (magenta), "#ffaa00" (orange)
```

### Speed Up Responses
Edit `config.yaml`:
```yaml
whisper_model: "tiny"        # Faster STT
ollama_model: "llama3.2:1b"  # Smaller, faster LLM
```

### Better Accuracy
Edit `config.yaml`:
```yaml
whisper_model: "small"   # Better STT
ollama_model: "llama3.2" # Full model (larger)
```

## Troubleshooting

### Wake word not working
```bash
echo $PICOVOICE_API_KEY  # Check if set
python3 jarvis.py --test # Test without wake word
```

### Microphone issues
```bash
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```
Grant permission: System Settings → Privacy & Security → Microphone

### Ollama not responding
```bash
ollama list                # Check if running
ollama pull llama3.2:3b    # Redownload model
```

### GUI not showing
```bash
python3 -c "import tkinter; print('OK')"  # Test tkinter
```

## File Structure

```
jarvis.py              # Main script
config.yaml            # Configuration
modules/               # Core modules
  ├── wake_word.py     # Wake word detection
  ├── speech_to_text.py # STT
  ├── llm_brain.py     # LLM
  ├── text_to_speech.py # TTS
  ├── tools.py         # System tools
  └── gui.py           # Interface
prompts/
  └── system_prompt.txt # LLM instructions
```

## Customization

### Add Custom Tool

1. Edit `modules/tools.py`:
```python
def _my_tool(self, data: Dict[str, Any]) -> tuple[bool, str]:
    """My custom tool."""
    param = data.get("param", "")
    # Your code here
    return True, "Success!"

# Add to __init__:
self.tool_handlers["my_tool"] = self._my_tool
```

2. Edit `prompts/system_prompt.txt` to teach LLM about it

### Change Wake Word

Available: jarvis, alexa, computer, hey google, ok google, picovoice, terminator

Edit `config.yaml`:
```yaml
wake_word: "computer"
```

## Performance Tips

- **M4 is fast!** You can use larger models for better results
- Use `small` Whisper model for best accuracy/speed balance
- Keep conversation history under 10 turns for faster responses
- Close unused apps to free up RAM for models

## Environment Variables

```bash
export PICOVOICE_API_KEY='your-key'          # Required for wake word
export OLLAMA_HOST='http://localhost:11434' # Change Ollama host
```

## Getting Help

- See `README.md` for full documentation
- See `QUICKSTART.md` for setup guide
- Run `python3 test_components.py` to test modules
- Check `prompts/system_prompt.txt` for available tools

## Fun Facts

- Everything runs locally (privacy!)
- No admin access required
- Works offline (except web searches)
- Customizable personality via system prompt
- Can control any AppleScript-compatible app

---

**Tip**: Say "Hey Jarvis" clearly with a slight pause before your command for best results!

