"""
Wake Word Detection Module
Uses Porcupine for "Hey Jarvis" detection.
"""
import struct
import pvporcupine
import sounddevice as sd
import numpy as np
from typing import Callable, Optional
import threading


class WakeWordDetector:
    """Wake word detector using Porcupine."""
    
    def __init__(
        self,
        access_key: str,
        keyword: str = "jarvis",
        sensitivity: float = 0.5
    ):
        """
        Initialize wake word detector.
        
        Args:
            access_key: Picovoice access key
            keyword: Wake word keyword (jarvis, alexa, etc.)
            sensitivity: Detection sensitivity (0.0 to 1.0)
        """
        self.access_key = access_key
        self.keyword = keyword
        self.sensitivity = sensitivity
        self.porcupine: Optional[pvporcupine.Porcupine] = None
        self.is_listening = False
        self.callback: Optional[Callable] = None
        self.listen_thread: Optional[threading.Thread] = None
        
        try:
            # Initialize Porcupine
            self.porcupine = pvporcupine.create(
                access_key=access_key,
                keywords=[keyword],
                sensitivities=[sensitivity]
            )
            print(f"Wake word detector initialized for '{keyword}'")
            print(f"Sample rate: {self.porcupine.sample_rate} Hz")
            print(f"Frame length: {self.porcupine.frame_length}")
        except Exception as e:
            print(f"Error initializing Porcupine: {e}")
            print("\nTo get a free API key:")
            print("1. Go to https://console.picovoice.ai/")
            print("2. Sign up for a free account")
            print("3. Create an access key")
            print("4. Add it to config.yaml or set PICOVOICE_API_KEY environment variable")
            raise
    
    def start(self, callback: Callable) -> None:
        """
        Start listening for wake word.
        
        Args:
            callback: Function to call when wake word detected
        """
        if self.is_listening:
            print("Already listening.")
            return
        
        self.callback = callback
        self.is_listening = True
        
        # Start listening thread
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        
        print(f"Listening for wake word '{self.keyword}'...")
    
    def stop(self) -> None:
        """Stop listening for wake word."""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        print("Wake word detection stopped.")
    
    def _listen_loop(self) -> None:
        """Main listening loop (runs in background thread)."""
        if not self.porcupine:
            return
        
        try:
            # Open audio stream
            with sd.InputStream(
                samplerate=self.porcupine.sample_rate,
                channels=1,
                dtype='int16',
                blocksize=self.porcupine.frame_length
            ) as stream:
                
                # Buffer to capture audio after wake word
                post_wake_buffer = []
                capturing_post_wake = False
                frames_to_capture = int(3.0 * self.porcupine.sample_rate / self.porcupine.frame_length)  # 3 seconds
                
                while self.is_listening:
                    # Read audio frame
                    audio_frame, overflowed = stream.read(self.porcupine.frame_length)
                    
                    if overflowed:
                        print("Audio buffer overflow!")
                    
                    # Convert to int16 array
                    pcm = audio_frame.flatten().astype(np.int16)
                    
                    # If capturing post-wake audio, add to buffer
                    if capturing_post_wake:
                        post_wake_buffer.append(pcm)
                        if len(post_wake_buffer) >= frames_to_capture:
                            capturing_post_wake = False
                            # Process captured audio
                            if self.callback and hasattr(self, 'post_wake_audio'):
                                self.post_wake_audio = np.concatenate(post_wake_buffer)
                    
                    # Process frame for wake word
                    keyword_index = self.porcupine.process(pcm)
                    
                    # Wake word detected!
                    if keyword_index >= 0:
                        print(f"Wake word '{self.keyword}' detected!")
                        # Start capturing audio after wake word
                        post_wake_buffer = []
                        capturing_post_wake = True
                        
                        if self.callback:
                            # Call callback in separate thread
                            threading.Thread(
                                target=self.callback,
                                daemon=True
                            ).start()
        
        except Exception as e:
            print(f"Error in wake word detection: {e}")
        finally:
            print("Wake word listener stopped.")
    
    def __del__(self):
        """Cleanup resources."""
        if self.porcupine:
            self.porcupine.delete()


if __name__ == "__main__":
    import time
    import os
    
    # Test wake word detector
    api_key = os.environ.get("PICOVOICE_API_KEY", "")
    
    if not api_key:
        print("Error: Set PICOVOICE_API_KEY environment variable")
        print("Get a free key at: https://console.picovoice.ai/")
        exit(1)
    
    def on_wake_word():
        print(">>> WAKE WORD DETECTED! <<<")
    
    detector = WakeWordDetector(access_key=api_key, keyword="jarvis")
    detector.start(callback=on_wake_word)
    
    print("Say 'Hey Jarvis' to test...")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        detector.stop()

