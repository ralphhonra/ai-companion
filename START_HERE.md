# 🎯 START HERE - Your JARVIS Voice Assistant

Welcome! Your JARVIS voice assistant system has been built and is ready to set up.

## 📁 What You Have

A complete, production-ready voice assistant system with:

- ✅ **Wake word detection** ("Hey Jarvis")
- ✅ **Speech recognition** (local, private)
- ✅ **Conversational AI** (Ollama LLM)
- ✅ **System control** (open apps, search files, control music)
- ✅ **Voice synthesis** (Mac text-to-speech)
- ✅ **Futuristic GUI** (terminal-style interface)
- ✅ **No admin required** (runs with user permissions)
- ✅ **100% local** (complete privacy)

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
cd ~/Desktop/ai-project
./setup.sh
```

This installs Ollama, downloads the AI model, and creates a Python virtual environment with all packages.

### Step 2: Get API Key (Free)

For wake word detection:

1. Visit: https://console.picovoice.ai/
2. Sign up (free account)
3. Copy your access key
4. Export it:

```bash
export PICOVOICE_API_KEY='your-key-here'
```

### Step 3: Run JARVIS

```bash
./run_jarvis.sh --test
```

**IMPORTANT:** Always use `./run_jarvis.sh` instead of `python jarvis.py`!  
(Or manually activate the virtual environment: `source venv/bin/activate`)

**Say: "What's the time?"** and JARVIS will respond! 🎉

---

## 📖 Documentation Guide

We've created comprehensive documentation for you:

| File | Purpose | When to Read |
|------|---------|--------------|
| **INSTALL_AND_RUN.md** | Complete installation guide | Read FIRST |
| **QUICKSTART.md** | 5-minute setup guide | After installation |
| **CHEATSHEET.md** | Command reference | Keep handy while using |
| **README.md** | Full documentation | For detailed understanding |
| **TESTING.md** | Testing procedures | If issues occur |

### Recommended Reading Order

1. **INSTALL_AND_RUN.md** ← Start here for installation
2. **QUICKSTART.md** ← Quick reference
3. **CHEATSHEET.md** ← Keep open while using JARVIS

---

## 🏗️ Architecture

```
jarvis.py (Main Orchestrator)
    ↓
    ├─→ wake_word.py (Listens for "Hey Jarvis")
    ├─→ speech_to_text.py (Converts speech to text)
    ├─→ llm_brain.py (Processes with AI)
    ├─→ tools.py (Executes system commands)
    ├─→ text_to_speech.py (Speaks responses)
    └─→ gui.py (Shows futuristic interface)
```

### Key Files

- `jarvis.py` - Main program (run this)
- `config.yaml` - All settings (customize here)
- `prompts/system_prompt.txt` - JARVIS personality
- `modules/` - Core components
- `setup.sh` - Automatic installation script
- `test_components.py` - Test individual parts

---

## 🎮 How to Use

### Mode 1: Test Mode (No Wake Word)

```bash
python3 jarvis.py --test
```

- GUI opens immediately
- Start speaking right away
- Perfect for testing

### Mode 2: Normal Mode (With Wake Word)

```bash
python3 jarvis.py
```

- Runs in background
- Say "Hey Jarvis" to activate
- GUI appears automatically

### Example Interaction

```
YOU: "Hey Jarvis"
[GUI opens with green terminal interface]

JARVIS: [Status: LISTENING]

YOU: "What's the time?"

JARVIS: [Status: THINKING]
JARVIS: [Status: SPEAKING]
JARVIS: "The current time is 3:42 PM, sir."

YOU: "Open Chrome"

JARVIS: "Opening Chrome, sir."
[Chrome opens]

YOU: "Goodbye"

JARVIS: "Goodbye, sir. Standing by."
[GUI closes]
```

---

## 🛠️ Available Commands

### Information Commands
- "What's the time?"
- "What's the date?"
- "Check battery"
- "How much disk space?"

### Application Control
- "Open [app name]" (Safari, Chrome, Spotify, etc.)
- "Launch [app name]"

### File Search
- "Search for [filename]"
- "Find [keyword] files"

### Music Control
- "Play music"
- "Pause"
- "Next track"
- "Volume up"

### Web Search
- "Search for [query]"
- "Look up [topic]"

### Conversation
- "How are you?"
- "What can you do?"
- "Tell me about yourself"

### Exit
- "Goodbye"
- "Exit"

---

## ⚙️ Configuration

Edit `config.yaml` to customize:

```yaml
# Wake word
wake_word: "jarvis"  # Options: jarvis, alexa, computer

# Voice
voice: "Samantha"  # Try: Alex, Daniel, Karen

# Speed
whisper_model: "base"  # tiny=fast, small=accurate
ollama_model: "llama3.2:3b"  # Or llama3.2:1b for faster

# GUI appearance
gui:
  text_color: "#00ff41"  # Matrix green
  background: "#000000"  # Black
```

---

## 🎨 Customization Examples

### Change to Blue Theme

```yaml
gui:
  text_color: "#00aaff"
```

### Use Male Voice

```yaml
voice: "Alex"  # or "Daniel"
```

### Faster Responses

```yaml
whisper_model: "tiny"
ollama_model: "llama3.2:1b"
```

### Better Accuracy

```yaml
whisper_model: "small"
```

---

## 🐛 Common Issues

### "PICOVOICE_API_KEY not found"

**Solution:**
```bash
export PICOVOICE_API_KEY='your-key'
python3 jarvis.py --test  # Works without API key
```

### "Could not connect to Ollama"

**Solution:**
```bash
ollama pull llama3.2:3b
ollama list  # Verify model exists
```

### Microphone not working

**Solution:**
- System Settings → Privacy & Security → Microphone
- Enable for Terminal

### Speech not recognized

**Solution:**
- Speak clearly and not too fast
- Reduce background noise
- Try: `whisper_model: "small"` in config

---

## 📚 Project Structure

```
ai-project/
├── START_HERE.md          ← You are here!
├── INSTALL_AND_RUN.md     ← Installation guide
├── QUICKSTART.md          ← Quick reference
├── CHEATSHEET.md          ← Command reference  
├── README.md              ← Full documentation
├── TESTING.md             ← Testing guide
│
├── jarvis.py              ← Main program
├── config.yaml            ← Configuration
├── requirements.txt       ← Python dependencies
├── setup.sh              ← Auto-installer
├── test_components.py     ← Component tests
│
├── modules/               ← Core components
│   ├── wake_word.py
│   ├── speech_to_text.py
│   ├── llm_brain.py
│   ├── text_to_speech.py
│   ├── tools.py
│   └── gui.py
│
└── prompts/
    └── system_prompt.txt  ← JARVIS personality
```

---

## 🎓 Learning Path

### Beginner
1. Run `./setup.sh`
2. Run `python3 jarvis.py --test`
3. Try basic commands from CHEATSHEET.md
4. Customize voice in config.yaml

### Intermediate
1. Modify GUI colors
2. Adjust performance settings
3. Add new voice commands
4. Customize system prompt

### Advanced
1. Add custom tools in `modules/tools.py`
2. Train custom wake word
3. Integrate with home automation
4. Create web-based UI

---

## 🚀 Next Steps

1. **Now:** Read `INSTALL_AND_RUN.md` and install
2. **Then:** Run `python3 jarvis.py --test`
3. **Next:** Customize `config.yaml`
4. **Finally:** Add your own features!

---

## 💡 Pro Tips

- Use `--test` mode for first run (skips wake word)
- Speak clearly with slight pauses
- M4 is powerful - try larger models for better results
- Keep `CHEATSHEET.md` open as reference
- Say "Hey Jarvis" with a slight pause: "Hey... Jarvis"
- Everything runs locally - no internet needed (except web searches)

---

## 🎯 Your First Session

Here's what to do right now:

```bash
# 1. Install (5 minutes)
cd ~/Desktop/ai-project
./setup.sh

# 2. Get API key (2 minutes)
# Visit: https://console.picovoice.ai/
# Export: export PICOVOICE_API_KEY='your-key'

# 3. Run test mode
python3 jarvis.py --test

# 4. Try these commands:
# "What's the time?"
# "How are you?"
# "Open Safari"
# "Goodbye"
```

---

## 📞 Need Help?

| Issue | Document | Section |
|-------|----------|---------|
| Installation problems | INSTALL_AND_RUN.md | Troubleshooting |
| Can't hear JARVIS | TESTING.md | Common Issues |
| Commands not working | CHEATSHEET.md | Commands List |
| Want to customize | README.md | Customization |
| Performance issues | QUICKSTART.md | Performance Tuning |

---

## ✨ Features Highlight

**Privacy:** Everything runs on your Mac - no cloud, no tracking

**Fast:** Optimized for M4 chip - instant responses

**Extensible:** Easy to add custom commands and tools

**No Admin:** Works with user permissions only

**Conversational:** Remembers context within session

**Professional:** Production-ready code with error handling

---

## 🎉 You're Ready!

Your JARVIS system is complete and ready to use. Start with `INSTALL_AND_RUN.md` to get it running.

Welcome to the future of voice assistants! 🚀

---

**Made with ⚡ for Mac M4**

*"Sometimes you gotta run before you can walk."* - Tony Stark

