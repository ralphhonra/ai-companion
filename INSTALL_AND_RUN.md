# Installation & First Run Guide

Complete step-by-step guide to get JARVIS running on your Mac M4.

## 🚀 Quick Install (5 minutes)

```bash
cd ~/Desktop/ai-project

# Run automatic setup
./setup.sh

# Get Picovoice API key (free)
# 1. Visit: https://console.picovoice.ai/
# 2. Sign up and copy your key
# 3. Export it:
export PICOVOICE_API_KEY='paste-your-key-here'

# Run JARVIS
python3 jarvis.py --test
```

Say: **"What's the time?"** to test!

---

## 📋 Detailed Installation

### Step 1: Install Ollama

Ollama runs the local LLM.

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download the model (this will take a few minutes)
ollama pull llama3.2:3b
```

**Verify:**
```bash
ollama list
# Should show: llama3.2:3b
```

### Step 2: Install Python Dependencies

```bash
cd ~/Desktop/ai-project

# Install requirements
pip3 install -r requirements.txt
```

This installs:
- `ollama` - Python client for Ollama
- `pvporcupine` - Wake word detection
- `faster-whisper` - Speech-to-text
- `sounddevice` - Audio recording
- `PyYAML` - Configuration
- `numpy`, `scipy` - Audio processing

**Note:** First run will download Whisper model (~140MB)

### Step 3: Get Picovoice API Key (Optional but Recommended)

Wake word detection requires a free API key.

1. Go to https://console.picovoice.ai/
2. Sign up (it's free!)
3. Go to "Access Keys"
4. Copy your access key
5. Export it:

```bash
export PICOVOICE_API_KEY='your-actual-key-here'

# Make it permanent:
echo 'export PICOVOICE_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**Verify:**
```bash
echo $PICOVOICE_API_KEY
# Should show your key
```

### Step 4: Grant Microphone Permissions

1. Open **System Settings**
2. Go to **Privacy & Security** → **Microphone**
3. Enable for **Terminal** (or your Python IDE)

**Test microphone:**
```bash
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```

### Step 5: Verify Installation

Run the component tests:

```bash
python3 test_components.py
```

You should see:
- ✓ Text-to-Speech working
- ✓ Tool Executor working
- ✓ Speech-to-Text model loaded
- ✓ Ollama connected
- ✓ Tkinter available
- ✓ PICOVOICE_API_KEY is set

---

## 🎬 First Run

### Option 1: Test Mode (Recommended for first run)

```bash
python3 jarvis.py --test
```

- GUI opens immediately
- No wake word needed
- Just start speaking!

**Try these commands:**
1. "What's the time?"
2. "What's the date?"
3. "How are you?"
4. "Open Safari"

Say "goodbye" to close.

### Option 2: Normal Mode (With Wake Word)

```bash
python3 jarvis.py
```

- Console shows "Listening for wake word..."
- Say **"Hey Jarvis"** to activate
- GUI opens when wake word detected

**Wake word tips:**
- Speak clearly
- Pause slightly: "Hey... Jarvis"
- Be in a quiet environment for first test

---

## ⚙️ Configuration

Before running, you might want to customize:

### Change Voice

```bash
# List available voices
say -v "?"

# Edit config.yaml
nano config.yaml
```

Change:
```yaml
voice: "Samantha"  # Try: Alex, Daniel, Karen, Victoria, Fiona
```

### Adjust Performance

For faster responses:
```yaml
whisper_model: "tiny"  # Faster but less accurate
ollama_model: "llama3.2:1b"  # Smaller model
```

For better accuracy:
```yaml
whisper_model: "small"  # Better accuracy
```

### Customize GUI

```yaml
gui:
  text_color: "#00ff41"  # Matrix green (default)
  # Try: "#00aaff" (blue), "#ff00ff" (magenta)
  width: 800  # Larger window
  height: 600
```

---

## 🐛 Troubleshooting Installation

### Issue: "ollama: command not found"

```bash
# Reinstall Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Or download from: https://ollama.com/download
```

### Issue: "Could not connect to Ollama"

```bash
# Check if Ollama is running
ollama list

# If not, start it
ollama serve &
```

### Issue: "pip: command not found"

```bash
# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Or use:
python3 -m ensurepip --upgrade
```

### Issue: "Permission denied" when installing packages

```bash
# Use --user flag
pip3 install --user -r requirements.txt

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Microphone not working

```bash
# Test microphone
python3 -c "import sounddevice as sd; sd.rec(16000, samplerate=16000, channels=1); import time; time.sleep(1); print('OK')"

# If fails, grant permissions in System Settings
```

### Issue: "No module named 'tkinter'"

```bash
# Reinstall Python from python.org (includes tkinter)
# Or install via Homebrew:
brew install python-tk@3.11
```

### Issue: Slow performance

```bash
# Check system resources
top

# Use smaller models in config.yaml:
whisper_model: "tiny"
ollama_model: "llama3.2:1b"

# Close unused applications
```

---

## 📊 What Gets Downloaded

| Component | Size | Purpose |
|-----------|------|---------|
| Ollama | ~200MB | LLM runtime |
| llama3.2:3b model | ~2GB | Language model |
| Whisper base model | ~140MB | Speech recognition |
| Python packages | ~300MB | Dependencies |
| **Total** | **~2.6GB** | |

**Note:** Downloads happen on first run, be patient!

---

## ✅ Verification Checklist

Before running JARVIS, verify:

- [ ] Ollama installed: `ollama --version`
- [ ] Model downloaded: `ollama list` shows llama3.2:3b
- [ ] Python 3.8+: `python3 --version`
- [ ] Dependencies installed: `pip3 list | grep ollama`
- [ ] API key set (optional): `echo $PICOVOICE_API_KEY`
- [ ] Microphone permission granted
- [ ] Audio working: `say "test"`

---

## 🎯 First Commands to Try

Once JARVIS is running:

### Information
- "What's the time?"
- "What's the date?"
- "Check battery"
- "How much disk space do I have?"

### Applications
- "Open Chrome"
- "Open Safari"
- "Launch Spotify"

### Files
- "Search for Python files"
- "Find presentation files"

### Music (if Music app is open)
- "Play music"
- "Next track"
- "Pause"

### Web
- "Search for Mac keyboard shortcuts"
- "Look up Python documentation"

### Conversation
- "How are you?"
- "What can you help me with?"
- "Tell me about yourself"

---

## 🚀 Running in Background

To keep JARVIS always listening:

### Option 1: Use screen

```bash
screen -S jarvis
python3 jarvis.py
# Press Ctrl+A, then D to detach

# To reattach:
screen -r jarvis
```

### Option 2: Use nohup

```bash
nohup python3 jarvis.py > jarvis.log 2>&1 &

# To stop:
ps aux | grep jarvis
kill <PID>
```

### Option 3: Create Launch Agent (Advanced)

See README.md for LaunchAgent configuration.

---

## 📚 Next Steps

After successful installation:

1. **Read** `QUICKSTART.md` for usage tips
2. **Review** `CHEATSHEET.md` for command reference
3. **Try** `TESTING.md` for comprehensive testing
4. **Customize** `config.yaml` to your liking
5. **Explore** adding custom tools in `modules/tools.py`

---

## 🆘 Still Having Issues?

1. Run component tests: `python3 test_components.py`
2. Check logs: Look for error messages
3. Try test mode first: `python3 jarvis.py --test`
4. Review `TESTING.md` for debugging steps
5. Check `README.md` troubleshooting section

---

**Enjoy your JARVIS! 🎉**

Made with ⚡ for Mac M4

