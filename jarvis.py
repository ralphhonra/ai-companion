#!/usr/bin/env python3
"""
JARVIS - Just A Rather Very Intelligent System
A voice-activated AI assistant for Mac.
"""
import os
import sys
import yaml
import time
import threading
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.wake_word import WakeWordDetector
from modules.speech_to_text import SpeechToText
from modules.llm_brain import LLMBrain
from modules.text_to_speech import TextToSpeech
from modules.tools import ToolExecutor
from modules.gui import JarvisGUI


class Jarvis:
    """Main Jarvis assistant orchestrator."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize Jarvis.
        
        Args:
            config_path: Path to configuration file
        """
        print("=" * 60)
        print("J.A.R.V.I.S. - Just A Rather Very Intelligent System")
        print("=" * 60)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Get Picovoice API key
        self.picovoice_key = os.environ.get("PICOVOICE_API_KEY", "")
        if not self.picovoice_key:
            print("\n⚠️  Warning: PICOVOICE_API_KEY not found in environment variables.")
            print("Wake word detection will not work without it.")
            print("\nTo get a free API key:")
            print("1. Go to https://console.picovoice.ai/")
            print("2. Sign up for a free account")
            print("3. Copy your access key")
            print("4. Export it: export PICOVOICE_API_KEY='your-key-here'")
            print("\nFor now, you can test without wake word by calling process_command() directly.\n")
        
        # Load system prompt
        prompt_path = Path(__file__).parent / "prompts" / "system_prompt.txt"
        with open(prompt_path, 'r') as f:
            system_prompt = f.read()
        
        # Initialize components
        print("\nInitializing components...")
        
        self.tts = TextToSpeech(
            voice=self.config['voice'],
            rate=self.config.get('speech_rate', 200)
        )
        print("✓ Text-to-Speech ready")
        
        self.stt = SpeechToText(
            model_size=self.config['whisper_model']
        )
        print("✓ Speech-to-Text ready")
        
        self.brain = LLMBrain(
            model=self.config['ollama_model'],
            system_prompt=system_prompt,
            max_history=self.config['conversation']['max_history']
        )
        print("✓ LLM Brain ready")
        
        self.tools = ToolExecutor()
        print("✓ Tool Executor ready")
        
        # GUI
        gui_config = self.config['gui']
        self.gui = JarvisGUI(
            width=gui_config['width'],
            height=gui_config['height'],
            bg_color=gui_config['background'],
            text_color=gui_config['text_color'],
            font_family=gui_config['font_family'],
            font_size=gui_config['font_size'],
            transparency=gui_config['transparency']
        )
        print("✓ GUI ready")
        
        # Wake word detector (optional)
        self.wake_detector = None
        if self.picovoice_key:
            try:
                self.wake_detector = WakeWordDetector(
                    access_key=self.picovoice_key,
                    keyword=self.config['wake_word'],
                    sensitivity=0.5
                )
                print("✓ Wake Word Detector ready")
            except Exception as e:
                print(f"✗ Wake Word Detector failed: {e}")
        
        # State
        self.is_active = False
        self.gui_thread = None
        self.timeout_timer = None
        
        print("\n✓ All systems operational!")
        print("=" * 60)
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            print("Using default configuration.")
            return self._default_config()
    
    def _default_config(self) -> dict:
        """Return default configuration."""
        return {
            'wake_word': 'jarvis',
            'whisper_model': 'base',
            'ollama_model': 'llama3.2:3b',
            'voice': 'Samantha',
            'speech_rate': 200,
            'audio': {
                'sample_rate': 16000,
                'channels': 1,
                'duration': 5,
                'silence_threshold': 0.01,
                'silence_duration': 1.5
            },
            'gui': {
                'background': '#000000',
                'text_color': '#00ff41',
                'width': 700,
                'height': 500,
                'font_size': 12,
                'font_family': 'Courier',
                'transparency': 0.95
            },
            'conversation': {
                'timeout': 30,
                'max_history': 10
            }
        }
    
    def start(self) -> None:
        """Start Jarvis (wake word listening mode)."""
        if not self.wake_detector:
            print("\n⚠️  Wake word detector not available.")
            print("You can test Jarvis by calling process_command() directly.")
            return
        
        print(f"\nListening for wake word: '{self.config['wake_word']}'")
        print("Say 'Hey Jarvis' to activate.")
        print("Press Ctrl+C to exit.\n")
        
        # Start wake word detection in background thread
        self.wake_detector.start(callback=self.on_wake_word_detected)
        
        try:
            # Keep main thread alive and available for GUI
            while True:
                time.sleep(0.1)
                # If GUI needs to be shown, show it on main thread
                if self.is_active and not self.gui.is_visible:
                    self.gui.set_close_callback(self.on_gui_close)
                    conversation_thread = threading.Thread(target=self.conversation_loop, daemon=True)
                    conversation_thread.start()
                    self.gui.show()  # Blocks until GUI closed
                    
        except KeyboardInterrupt:
            print("\n\nShutting down JARVIS...")
            self.shutdown()
    
    def on_wake_word_detected(self) -> None:
        """Handle wake word detection (called from wake word thread)."""
        if self.is_active:
            return  # Already active
        
        print("\n>>> Wake word detected! <<<")
        self.is_active = True
        # Main thread loop will pick this up and show GUI
    
    
    def conversation_loop(self) -> None:
        """Main conversation loop."""
        # Wait for GUI to be ready
        print("Conversation loop started, waiting for GUI...")
        while not self.gui.is_visible and self.is_active:
            time.sleep(0.1)
        
        print("GUI visible, starting conversation...")
        
        while self.is_active and self.gui.is_visible:
            try:
                # Listen for user input
                self.gui.set_status("LISTENING")
                print("Status: LISTENING - Speak now...")
                
                audio_config = self.config['audio']
                user_text = self.stt.listen(
                    duration=audio_config['duration'],
                    silence_threshold=audio_config['silence_threshold'],
                    silence_duration=audio_config['silence_duration']
                )
                
                print(f"📝 Transcribed: '{user_text}'")
                
                if not user_text or len(user_text.strip()) < 2:
                    # No speech detected, timeout after a while
                    print("⚠️  No speech detected or text too short, listening again...")
                    self._start_timeout()
                    continue
                
                print(f"✓ Valid input detected: '{user_text}'")
                
                # Cancel timeout since we got input
                self._cancel_timeout()
                
                # Display user input (cleaned up)
                display_text = user_text.strip()
                self.gui.add_text(display_text, "USER: ")
                
                # Show what we're processing
                print(f"🤖 Processing: '{display_text}'")
                
                # Check for exit commands
                if any(word in user_text.lower() for word in ['goodbye', 'exit', 'quit', 'close']):
                    self.gui.set_status("SPEAKING")
                    response = "Goodbye, sir. Standing by."
                    self.gui.type_text(response, "JARVIS: ")
                    self.tts.speak(response, blocking=True)
                    time.sleep(1)
                    self.gui.hide()
                    break
                
                # Process with LLM
                self.process_command(user_text)
                
                # Start timeout timer
                self._start_timeout()
                
            except Exception as e:
                print(f"Error in conversation loop: {e}")
                self.gui.set_status("ERROR")
                time.sleep(2)
    
    def process_command(self, user_text: str) -> None:
        """
        Process a user command.
        
        Args:
            user_text: User's text input
        """
        # Get LLM response
        self.gui.set_status("THINKING")
        llm_response = self.brain.process(user_text)
        
        print(f"LLM Response: {llm_response}")
        
        # Execute tools
        success, result = self.tools.execute(llm_response)
        
        # Speak response
        self.gui.set_status("SPEAKING")
        
        # Clean up response - remove any JSON artifacts
        response_text = result.strip()
        
        # If response still looks like JSON, extract the response field
        if response_text.startswith('{') and '"response"' in response_text:
            try:
                import json
                data = json.loads(response_text)
                response_text = data.get('response', 'Task completed.')
            except:
                # If parsing fails, try to extract text manually
                response_text = "Task completed."
        
        # Get first line for speaking, full text for display
        speak_text = response_text.split('\n')[0] if '\n' in response_text else response_text
        
        # Start speaking immediately (non-blocking)
        speech_thread = self.tts.speak_async(speak_text)
        
        # Type text while speaking
        self.gui.type_text(speak_text, "JARVIS: ")
        
        # Wait for speech to complete
        speech_thread.join()
        
        # Show additional details if any
        if '\n' in result:
            details = '\n'.join(result.split('\n')[1:])
            self.gui.add_text(details, "")
        
        self.gui.set_status("READY")
    
    def _start_timeout(self) -> None:
        """Start inactivity timeout."""
        self._cancel_timeout()
        
        timeout = self.config['conversation']['timeout']
        self.timeout_timer = threading.Timer(timeout, self._on_timeout)
        self.timeout_timer.daemon = True
        self.timeout_timer.start()
    
    def _cancel_timeout(self) -> None:
        """Cancel inactivity timeout."""
        if self.timeout_timer:
            self.timeout_timer.cancel()
            self.timeout_timer = None
    
    def _on_timeout(self) -> None:
        """Handle inactivity timeout."""
        if self.is_active and self.gui.is_visible:
            print("Inactivity timeout - closing GUI")
            self.gui.hide()
    
    def on_gui_close(self) -> None:
        """Handle GUI close event."""
        self.is_active = False
        self._cancel_timeout()
        self.brain.reset_conversation()
        print("Session ended. Listening for wake word...\n")
    
    def shutdown(self) -> None:
        """Shutdown Jarvis."""
        self.is_active = False
        self._cancel_timeout()
        
        if self.wake_detector:
            self.wake_detector.stop()
        
        if self.gui.is_visible:
            self.gui.hide()
        
        print("JARVIS offline. Goodbye.")


def main():
    """Main entry point."""
    # Check for config file
    config_path = Path(__file__).parent / "config.yaml"
    
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)
    
    # Create Jarvis instance
    jarvis = Jarvis(str(config_path))
    
    # Check if testing mode (command line argument)
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("\n=== TEST MODE ===")
        print("Testing without wake word detection.\n")
        
        # Set up GUI callback
        jarvis.is_active = True
        jarvis.gui.set_close_callback(jarvis.on_gui_close)
        
        # Start conversation loop in background thread
        # (GUI must run on main thread for macOS compatibility)
        conversation_thread = threading.Thread(target=jarvis.conversation_loop, daemon=True)
        conversation_thread.start()
        
        # Run GUI on main thread (this blocks until GUI is closed)
        jarvis.gui.show()
        
        # Ensure clean exit after GUI closes in test mode
        print("\n✓ JARVIS shutdown complete. Goodbye!")
        sys.exit(0)
    else:
        # Normal mode with wake word
        jarvis.start()


if __name__ == "__main__":
    main()

