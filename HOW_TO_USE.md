# How to Use JARVIS - Simple Guide

## 🚀 Quick Start

```bash
./run_jarvis.sh
```

That's it! The GUI opens and JARVIS is ready.

## 🗣️ How to Talk to JARVIS

### Every Command Must Start with "Hey Jarvis"

Say everything in ONE breath:

✅ **Correct:**
```
"Hey Jarvis, what's the time?"
"Hey Jarvis, open Chrome"
"Hey Jarvis, play music on YouTube"
"Hey Jarvis, check my battery"
"Hey Jarvis, goodbye"
```

❌ **Wrong (will be ignored):**
```
"What's the time?"  → [IGNORED]
"Open Chrome"  → [IGNORED]
```

## 💡 How It Works

1. **Run JARVIS:**
   ```bash
   ./run_jarvis.sh
   ```

2. **GUI opens with greeting:**
   ```
   JARVIS: "Systems online. Say 'Hey Jarvis' before each command, sir."
   ```

3. **Say your command:**
   ```
   YOU: "Hey Jarvis, what's the time?"
   JARVIS: "The current time is 3:42 PM, sir."
   ```

4. **Another command:**
   ```
   YOU: "Hey Jarvis, open Safari"
   JARVIS: "Opening Safari, sir."
   ```

5. **To close:**
   ```
   YOU: "Hey Jarvis, goodbye"
   JARVIS: "Farewell, sir. Standing by."
   ```

## 🎯 Key Points

- **Say "Hey Jarvis" every time** (at the start of each command)
- **Say it all together** ("Hey Jarvis, [command]" in one sentence)
- **Pause after speaking** (1 second of silence triggers processing)
- **Commands without "Hey Jarvis"** will be ignored

## 📋 Example Session

```bash
./run_jarvis.sh
```

```
[GUI opens]
🔊 Tink!
JARVIS: "Systems online. Say 'Hey Jarvis' before each command, sir."

YOU: "Hey Jarvis, what's the time?"
JARVIS: "The current time is 3:42 PM, sir."

YOU: "Hey Jarvis, open Chrome"
JARVIS: "Opening Chrome, sir."

YOU: "Hey Jarvis, play lofi music on YouTube"
JARVIS: "Certainly, sir. Opening YouTube..."

YOU: "Check battery"  ← FORGOT "Hey Jarvis"!
[Shows: [IGNORED] (Please say 'Hey Jarvis' before your command)]

YOU: "Hey Jarvis, check battery"  ← CORRECT!
JARVIS: "Your battery is at 75%, sir."

YOU: "Hey Jarvis, goodbye"
JARVIS: "Farewell, sir. Standing by."
🔇 Pop!
[GUI closes]
```

## 🎤 Speaking Tips

1. **Say it naturally:** "Hey Jarvis, what's the time?"
2. **Brief pause after "Jarvis":** "Hey Jarvis, [pause] open Chrome"
3. **One sentence:** Don't split into two separate utterances
4. **Wait 1 second** after finishing for JARVIS to process

## 🔧 Troubleshooting

### "Command gets ignored"
→ Make sure you said "Hey Jarvis" at the start

### "Only captures first part"
→ Say it slower with a slight pause after "Jarvis"

### "Nothing happens"
→ Check if GUI is open and status shows "LISTENING"

---

**Remember:** "Hey Jarvis" before EVERY command! 🎯


