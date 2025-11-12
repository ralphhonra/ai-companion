# Quick Start Guide

Get JARVIS up and running in 5 minutes!

## Automatic Setup (Recommended)

```bash
cd ai-project
chmod +x setup.sh
./setup.sh
```

This will:
- Check Python installation
- Install/check Ollama
- Download the LLM model
- Install Python dependencies
- Check microphone permissions

## Manual Setup

### 1. Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
```

### 2. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Get Picovoice API Key

1. Go to https://console.picovoice.ai/
2. Sign up (free)
3. Copy your access key
4. Export it:

```bash
export PICOVOICE_API_KEY='your-key-here'

# Add to shell profile to persist:
echo 'export PICOVOICE_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 4. Grant Microphone Access

- Open System Settings
- Go to Privacy & Security → Microphone
- Enable for Terminal (or your Python IDE)

## Running JARVIS

### Test Mode (No Wake Word)

```bash
python3 jarvis.py --test
```

GUI opens immediately. Start speaking!

### Normal Mode (Wake Word)

```bash
python3 jarvis.py
```

Say "Hey Jarvis" to activate.

## First Commands to Try

```
"What's the time?"
"What's the date?"
"Open Safari"
"Search for Python files"
"How are you?"
```

## Troubleshooting

### "PICOVOICE_API_KEY not found"

```bash
# Check if set:
echo $PICOVOICE_API_KEY

# If empty, export it:
export PICOVOICE_API_KEY='your-key-here'
```

### "Could not connect to Ollama"

```bash
# Check if Ollama is running:
ollama list

# If not found, reinstall:
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b
```

### "Microphone not working"

```bash
# Test microphone:
python3 -c "import sounddevice as sd; print(sd.query_devices())"

# Grant permissions in System Settings
```

### Model Download Times

First run will download Whisper model (~140MB):
- `tiny`: ~40MB (fastest, less accurate)
- `base`: ~140MB (balanced) ← default
- `small`: ~480MB (better accuracy)

Change in `config.yaml`:
```yaml
whisper_model: "tiny"  # or "small", "medium"
```

## Performance Tuning

### Faster Responses

```yaml
whisper_model: "tiny"
ollama_model: "llama3.2:1b"
```

### Better Accuracy

```yaml
whisper_model: "small"
ollama_model: "llama3.2"
```

## Next Steps

- Customize `config.yaml` (voices, colors, timeout)
- Read `README.md` for full documentation
- Add custom tools in `modules/tools.py`
- Modify system prompt in `prompts/system_prompt.txt`

Enjoy your JARVIS! 🚀

