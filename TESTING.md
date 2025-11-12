# Testing Guide for JARVIS

This guide walks you through testing JARVIS step-by-step.

## Prerequisites

Before testing, ensure you have:

1. ✅ Python 3.8+ installed
2. ✅ Ollama installed and running
3. ✅ Model downloaded (`ollama pull llama3.2:3b`)
4. ✅ Python dependencies installed (`pip3 install -r requirements.txt`)
5. ✅ Picovoice API key exported (optional, for wake word)
6. ✅ Microphone permissions granted

## Testing Strategy

We'll test components individually first, then the full system.

### Stage 1: Component Tests

Run the test suite:

```bash
python3 test_components.py
```

This tests each module independently:

1. **Text-to-Speech** - You should hear "Hello, I am JARVIS..."
2. **Tool Executor** - Shows current time, date, battery
3. **Speech-to-Text** - Checks if Whisper model loads
4. **LLM Brain** - Tests Ollama connection and response
5. **GUI** - Verifies Tkinter is available
6. **Wake Word** - Checks Picovoice API key

#### Test Individual Components

```bash
# Test just TTS
python3 -m modules.text_to_speech

# Test just GUI
python3 -m modules.gui

# Test just Wake Word (requires API key)
python3 -m modules.wake_word
```

### Stage 2: Integration Test (Without Wake Word)

Test the full system without wake word detection:

```bash
python3 jarvis.py --test
```

**Expected behavior:**
1. GUI window opens immediately
2. Status shows "LISTENING" 
3. You speak a command
4. Status changes to "THINKING"
5. Status changes to "SPEAKING"
6. Response appears with typing animation
7. You hear the response spoken

**Test commands:**
```
"What's the time?"
"What's the date?"  
"How are you?"
"Open Safari"
```

Say "goodbye" to close.

### Stage 3: Full System Test (With Wake Word)

Test with wake word detection:

```bash
python3 jarvis.py
```

**Expected behavior:**
1. Console shows "Listening for wake word..."
2. Say "Hey Jarvis"
3. GUI opens immediately
4. Continue as in Stage 2

### Stage 4: Stress Testing

Test various scenarios:

#### 1. Multiple Interactions
```bash
python3 jarvis.py --test
```

Try a conversation:
```
"What's the time?"
[Wait for response]
"And what's the date?"
[Wait for response]
"Thanks"
```

#### 2. Tool Commands
```
"Open Chrome"
"Search for Python tutorials"
"Check battery"
"Find Python files"
```

#### 3. Conversational
```
"Hello"
"How are you?"
"What can you help me with?"
"Tell me about yourself"
```

#### 4. Edge Cases
```
[Say nothing - should timeout after 30s]
[Say gibberish - should still respond]
[Interrupt during response - say "stop"]
```

## Verification Checklist

### Component Level

- [ ] TTS speaks clearly with chosen voice
- [ ] STT transcribes speech accurately
- [ ] LLM generates JSON responses
- [ ] Tools execute without errors
- [ ] GUI opens and displays properly
- [ ] Wake word triggers reliably

### Integration Level

- [ ] Wake word triggers GUI
- [ ] Speech is transcribed correctly
- [ ] LLM understands commands
- [ ] Tools execute successfully
- [ ] TTS speaks responses
- [ ] GUI shows all interactions
- [ ] Conversation context maintained
- [ ] Timeout works (30s inactivity)
- [ ] Manual close works (X button)
- [ ] "Goodbye" closes session

### Performance

- [ ] Wake word latency < 1s
- [ ] STT latency < 3s
- [ ] LLM response < 5s
- [ ] TTS starts immediately
- [ ] GUI is responsive
- [ ] No crashes or freezes

## Common Issues & Solutions

### Issue: No sound from TTS

**Solution:**
```bash
# Test Mac 'say' command
say "test"

# Check volume
osascript -e 'output volume of (get volume settings)'
```

### Issue: STT not recognizing speech

**Solutions:**
- Speak clearly and not too fast
- Reduce background noise
- Increase recording duration in `config.yaml`:
  ```yaml
  audio:
    duration: 7  # Increase from 5
  ```
- Try smaller model for faster processing:
  ```yaml
  whisper_model: "tiny"
  ```

### Issue: LLM responses are slow

**Solutions:**
- Use smaller model: `llama3.2:1b`
- Reduce conversation history:
  ```yaml
  conversation:
    max_history: 5
  ```
- Close other apps to free RAM

### Issue: Wake word false positives

**Solution:**
- Increase sensitivity in code:
  ```python
  # In jarvis.py, change:
  sensitivity=0.7  # Instead of 0.5
  ```

### Issue: GUI doesn't show

**Solutions:**
```bash
# Check if display is accessible
python3 -c "import tkinter; root = tkinter.Tk(); print('OK')"

# Check screen resolution
system_profiler SPDisplaysDataType
```

## Debugging Mode

Enable verbose logging:

```python
# Add to jarvis.py after imports:
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Benchmarks (M4)

Expected timings on Mac M4:

| Operation | Expected Time |
|-----------|---------------|
| Wake word detection | < 500ms |
| STT (base model) | 2-3s |
| LLM response | 2-5s |
| TTS | Immediate |
| GUI open | < 500ms |
| Total interaction | 5-10s |

## Automated Testing Script

Create `run_tests.sh`:

```bash
#!/bin/bash

echo "=== JARVIS Test Suite ==="

echo "\n1. Checking dependencies..."
python3 -c "import ollama; import pvporcupine; import faster_whisper; print('✓ All imports OK')"

echo "\n2. Testing components..."
python3 test_components.py

echo "\n3. Manual test required:"
echo "Run: python3 jarvis.py --test"
echo "Try saying: 'What's the time?'"

echo "\nTests complete!"
```

## Test Logs

Record your test results:

```bash
# Create test log
python3 jarvis.py --test 2>&1 | tee test_log.txt
```

## Next Steps After Testing

Once all tests pass:

1. ✅ Customize `config.yaml` to your preferences
2. ✅ Modify `prompts/system_prompt.txt` for personality
3. ✅ Add custom tools in `modules/tools.py`
4. ✅ Set up autostart (optional):
   ```bash
   # Add to ~/.zshrc:
   # nohup python3 ~/Desktop/ai-project/jarvis.py > /dev/null 2>&1 &
   ```

## Reporting Issues

If you encounter issues:

1. Check this testing guide
2. Review `README.md` troubleshooting section
3. Check logs for error messages
4. Verify all prerequisites are met
5. Try test mode first (`--test` flag)

---

**Happy Testing! 🎯**

