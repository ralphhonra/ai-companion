#!/usr/bin/env python3
"""
Test script for individual JARVIS components.
Run this to verify each module works independently.
"""
import sys
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))


def test_tts():
    """Test Text-to-Speech."""
    print("\n" + "=" * 60)
    print("Testing Text-to-Speech (Mac 'say' command)")
    print("=" * 60)
    
    from modules.text_to_speech import TextToSpeech
    
    tts = TextToSpeech(voice="Samantha")
    
    print("Available voices (first 5):", tts.list_voices()[:5])
    print("\nSpeaking: 'Hello, I am JARVIS. All systems operational.'")
    
    tts.speak("Hello, I am JARVIS. All systems operational.", blocking=True)
    
    print("✓ Text-to-Speech working!\n")


def test_tools():
    """Test Tool Executor."""
    print("\n" + "=" * 60)
    print("Testing Tool Executor")
    print("=" * 60)
    
    from modules.tools import ToolExecutor
    
    executor = ToolExecutor()
    
    # Test get_info (time)
    print("\nTest 1: Get current time")
    response = '{"tool": "get_info", "info_type": "time", "response": "Getting current time."}'
    success, result = executor.execute(response)
    print(f"Success: {success}")
    print(f"Result: {result}")
    
    # Test get_info (date)
    print("\nTest 2: Get current date")
    response = '{"tool": "get_info", "info_type": "date", "response": "Getting current date."}'
    success, result = executor.execute(response)
    print(f"Success: {success}")
    print(f"Result: {result}")
    
    # Test get_info (battery)
    print("\nTest 3: Get battery status")
    response = '{"tool": "get_info", "info_type": "battery", "response": "Checking battery."}'
    success, result = executor.execute(response)
    print(f"Success: {success}")
    print(f"Result: {result}")
    
    print("\n✓ Tool Executor working!\n")


def test_stt():
    """Test Speech-to-Text."""
    print("\n" + "=" * 60)
    print("Testing Speech-to-Text (Faster-Whisper)")
    print("=" * 60)
    
    from modules.speech_to_text import SpeechToText
    
    print("Loading Whisper model (this may take a moment)...")
    stt = SpeechToText(model_size="base")
    
    print("\n✓ Speech-to-Text model loaded!")
    print("\nTo test STT, run:")
    print("  python3 -c \"from modules.speech_to_text import SpeechToText; stt = SpeechToText(); print('Speak now...'); print('You said:', stt.listen())\"")
    print("")


def test_llm():
    """Test LLM Brain."""
    print("\n" + "=" * 60)
    print("Testing LLM Brain (Ollama)")
    print("=" * 60)
    
    import ollama
    
    # Check if Ollama is running
    try:
        models = ollama.list()
        print("✓ Ollama is running")
        print(f"Available models: {len(models.get('models', []))}")
        
        # Check if our model exists
        model_name = "llama3.2:3b"
        has_model = any(m['name'].startswith(model_name) for m in models.get('models', []))
        
        if has_model:
            print(f"✓ Model '{model_name}' found")
            
            # Test a simple query
            print("\nTesting simple query...")
            from modules.llm_brain import LLMBrain
            
            system_prompt = """You are JARVIS. Respond in JSON format:
            {"tool": "none", "response": "Your response here"}"""
            
            brain = LLMBrain(model=model_name, system_prompt=system_prompt)
            response = brain.process("Hello, introduce yourself briefly")
            
            print(f"Response: {response[:200]}...")
            print("\n✓ LLM Brain working!")
        else:
            print(f"✗ Model '{model_name}' not found")
            print(f"Run: ollama pull {model_name}")
            
    except Exception as e:
        print(f"✗ Error connecting to Ollama: {e}")
        print("\nTo install Ollama:")
        print("  curl -fsSL https://ollama.com/install.sh | sh")
        print("  ollama pull llama3.2:3b")
    
    print("")


def test_gui():
    """Test GUI."""
    print("\n" + "=" * 60)
    print("Testing GUI (Tkinter)")
    print("=" * 60)
    
    import tkinter as tk
    
    print("✓ Tkinter available")
    
    print("\nTo test GUI, run:")
    print("  python3 -m modules.gui")
    print("")


def test_wake_word():
    """Test Wake Word Detector."""
    print("\n" + "=" * 60)
    print("Testing Wake Word Detector (Porcupine)")
    print("=" * 60)
    
    import os
    
    api_key = os.environ.get("PICOVOICE_API_KEY", "")
    
    if not api_key:
        print("✗ PICOVOICE_API_KEY not set")
        print("\nTo get a free API key:")
        print("1. Go to: https://console.picovoice.ai/")
        print("2. Sign up for a free account")
        print("3. Export it: export PICOVOICE_API_KEY='your-key-here'")
    else:
        print("✓ PICOVOICE_API_KEY is set")
        print("\nTo test wake word detection, run:")
        print("  python3 -m modules.wake_word")
    
    print("")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  JARVIS Component Test Suite")
    print("=" * 60)
    
    tests = [
        ("Text-to-Speech", test_tts),
        ("Tool Executor", test_tools),
        ("Speech-to-Text", test_stt),
        ("LLM Brain", test_llm),
        ("GUI", test_gui),
        ("Wake Word", test_wake_word),
    ]
    
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1].lower()
        for name, test_func in tests:
            if test_name in name.lower():
                test_func()
                return
        print(f"Unknown test: {sys.argv[1]}")
        print(f"Available tests: {', '.join([name for name, _ in tests])}")
    else:
        # Run all tests
        for name, test_func in tests:
            try:
                test_func()
            except KeyboardInterrupt:
                print("\n\nTests interrupted by user.")
                break
            except Exception as e:
                print(f"\n✗ {name} failed: {e}\n")
        
        print("=" * 60)
        print("  Test Suite Complete")
        print("=" * 60)
        print("\nIf all tests passed, run: python3 jarvis.py --test")
        print("")


if __name__ == "__main__":
    main()

