# Common Errors & Quick Fixes

## Error: "ModuleNotFoundError: No module named 'yaml'" (or any module)

### What Happened
You ran `python3 jarvis.py` directly, but the packages are installed in the virtual environment.

### Quick Fix
Use the launcher script:
```bash
./run_jarvis.sh --test
```

### Or Manually
```bash
source venv/bin/activate
python jarvis.py --test
```

### Why?
After running `./setup.sh`, all Python packages are installed in `venv/` (virtual environment), not system-wide. You must activate it first!

---

## Error: "externally-managed-environment"

### What Happened
Modern macOS protects system Python from modifications.

### Quick Fix
Run the updated setup script:
```bash
./setup.sh
```

It now automatically creates a virtual environment.

---

## Error: "PICOVOICE_API_KEY not found"

### What Happened
Wake word detection requires a free API key.

### Quick Fix
```bash
# Get key from: https://console.picovoice.ai/
export PICOVOICE_API_KEY='your-key-here'

# Or test without wake word:
./run_jarvis.sh --test
```

---

## Error: "NSWindow should only be instantiated on the main thread"

### What Happened
macOS requires GUI windows to be created on the main thread. This is a Tkinter/macOS requirement.

### Quick Fix
Already fixed in the latest version! The code now properly runs the GUI on the main thread.

If you're seeing this error with old code:
```bash
git pull  # Get latest version
./run_jarvis.sh --test
```

---

## Error: "ModuleNotFoundError: No module named '_tkinter'"

### What Happened
Homebrew Python doesn't include tkinter by default.

### Quick Fix
```bash
brew install python-tk@3.13
```

Then try running JARVIS again.

---

## Error: "Could not connect to Ollama"

### What Happened
Ollama isn't running or model isn't downloaded.

### Quick Fix
```bash
ollama pull llama3.2:3b
ollama list  # Verify model exists
```

---

## Error: Microphone not working

### Quick Fix
1. System Settings → Privacy & Security → Microphone
2. Enable for Terminal
3. Restart terminal and try again

---

## Error: "command not found: ./run_jarvis.sh"

### Quick Fix
Make it executable:
```bash
chmod +x run_jarvis.sh
./run_jarvis.sh --test
```

---

## Pro Tip: Always Use the Launcher

Instead of remembering to activate the virtual environment, just use:

```bash
./run_jarvis.sh --test    # Test mode
./run_jarvis.sh           # Normal mode
```

The launcher handles everything automatically!

---

## Still Having Issues?

Check these files:
- `FIXED_SETUP.md` - Setup issues
- `TESTING.md` - Detailed troubleshooting
- `README.md` - Full documentation

