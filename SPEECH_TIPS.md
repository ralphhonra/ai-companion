# Speech Recognition Tips

## 🎤 For Best Accuracy

### Speaking Technique
1. **Speak at normal pace** - Not too fast, not too slow
2. **Pause between commands** - Give JARVIS 2 seconds of silence to finish recording
3. **Use clear enunciation** - Especially for app names
4. **Stay close to mic** - Within 1-2 feet is ideal
5. **Reduce background noise** - Music, TV, fans can interfere

### When JARVIS Mishears

If JARVIS consistently mishears certain words:

**Instead of:**
- "Open QuickTime" (often misheard)

**Try:**
- "Open the time app"
- "Launch QuickTime Player" (full name)
- "Open recorder app"

**Instead of:**
- "Open Chrome"

**Try:**
- "Open Google Chrome" (full name)
- "Launch the browser"

### Common App Name Alternatives

| Instead of | Try |
|-----------|-----|
| QuickTime | "time player" or "recorder" |
| GarageBand | "garage" or "music app" |
| System Settings | "system preferences" |
| Activity Monitor | "activity app" |

## 📊 Model Comparison

Your current setup:

| Model | Accuracy | Speed | Size |
|-------|----------|-------|------|
| **small** ✓ | 95%+ | 3-4s | 480MB |
| base | 90% | 2-3s | 140MB |
| tiny | 80% | 1-2s | 40MB |

You're now using **small** for best accuracy!

## 🔧 If Still Having Issues

### 1. Check Microphone Level
```bash
# Test mic input
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```

### 2. Adjust Recording Sensitivity

Edit `config.yaml`:
```yaml
audio:
  silence_threshold: 0.003  # Lower = more sensitive (default: 0.005)
  silence_duration: 2.5     # Wait longer before stopping (default: 2.0)
```

### 3. Use Longer Recording Duration
```yaml
audio:
  duration: 10  # Allow longer commands (default: 8)
```

### 4. Try Different Whisper Model

If too slow, go back to "base":
```yaml
whisper_model: "base"
```

If need max accuracy, upgrade to "medium":
```yaml
whisper_model: "medium"  # ~1.5GB, slower but very accurate
```

## 💡 Pro Tips

1. **Wait for "🎤 Recording"** before speaking
2. **Say full app names** (e.g., "Google Chrome" not "Chrome")
3. **Spell uncommon words** if misheard repeatedly
4. **Use synonyms** if one phrase doesn't work
5. **Speak in complete sentences** for better context

## Example Good Commands

✅ "Open Google Chrome please"
✅ "What is the current time"
✅ "Launch Calendar application"
✅ "Search for Python files"
✅ "Check my battery status"

❌ "Chrome" (too short)
❌ "Wat time?" (unclear)
❌ "Cal" (ambiguous)

---

**Remember**: The "small" model is much better at understanding different accents and handling background noise!

