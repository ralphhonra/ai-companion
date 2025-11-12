"""
Text-to-Speech Module
Uses Mac's built-in 'say' command for voice synthesis.
"""
import subprocess
import threading
from typing import Optional


class TextToSpeech:
    """Wrapper for Mac's 'say' command."""
    
    def __init__(self, voice: str = "Samantha", rate: int = 200):
        """
        Initialize TTS.
        
        Args:
            voice: Mac voice name (e.g., "Samantha", "Alex", "Daniel")
            rate: Speech rate in words per minute (default: 200)
        """
        self.voice = voice
        self.rate = rate
        self.current_process: Optional[subprocess.Popen] = None
        
    def speak(self, text: str, blocking: bool = False) -> None:
        """
        Speak the given text.
        
        Args:
            text: Text to speak
            blocking: If True, wait for speech to complete
        """
        if not text or not text.strip():
            return
            
        # Stop any ongoing speech
        self.stop()
        
        try:
            cmd = ["say", "-v", self.voice, "-r", str(self.rate), text]
            
            if blocking:
                subprocess.run(cmd, check=True)
            else:
                # Run in background
                self.current_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def speak_async(self, text: str) -> threading.Thread:
        """
        Speak text in a separate thread.
        
        Args:
            text: Text to speak
            
        Returns:
            Thread object
        """
        thread = threading.Thread(target=self.speak, args=(text, True))
        thread.daemon = True
        thread.start()
        return thread
    
    def stop(self) -> None:
        """Stop any ongoing speech."""
        try:
            # Kill the say process if running
            if self.current_process and self.current_process.poll() is None:
                self.current_process.terminate()
                self.current_process.wait(timeout=1)
        except Exception:
            pass
        finally:
            self.current_process = None
    
    def is_speaking(self) -> bool:
        """Check if currently speaking."""
        return (self.current_process is not None and 
                self.current_process.poll() is None)
    
    @staticmethod
    def list_voices() -> list:
        """Get list of available Mac voices."""
        try:
            result = subprocess.run(
                ["say", "-v", "?"],
                capture_output=True,
                text=True,
                check=True
            )
            voices = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    # Parse voice name (first word)
                    voice_name = line.split()[0]
                    voices.append(voice_name)
            return voices
        except Exception as e:
            print(f"Error listing voices: {e}")
            return ["Samantha", "Alex", "Daniel"]  # Defaults


if __name__ == "__main__":
    # Test TTS
    tts = TextToSpeech()
    print("Available voices:", tts.list_voices()[:5])
    print("Speaking test...")
    tts.speak("Hello, I am Jarvis. All systems operational.", blocking=True)
    print("Done!")

