"""
Speech-to-Text Module
Uses faster-whisper for local speech recognition.
"""
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from typing import Optional
import tempfile
import wave


class SpeechToText:
    """Speech recognition using faster-whisper."""
    
    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8"
    ):
        """
        Initialize speech-to-text.
        
        Args:
            model_size: Model size (tiny, base, small, medium, large)
            device: Device to use (cpu, cuda)
            compute_type: Computation type (int8, float16, float32)
        """
        print(f"Loading Whisper model '{model_size}'...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.sample_rate = 16000
        print("Whisper model loaded.")
    
    def record_audio(
        self,
        duration: int = 5,
        silence_threshold: float = 0.01,
        silence_duration: float = 1.5,
        min_duration: float = 1.0
    ) -> Optional[np.ndarray]:
        """
        Record audio from microphone with improved silence detection.
        
        Args:
            duration: Maximum recording duration in seconds
            silence_threshold: Threshold for silence detection (lower = more sensitive)
            silence_duration: Seconds of silence before stopping
            min_duration: Minimum recording duration (ensures we capture at least this much)
            
        Returns:
            Audio data as numpy array or None if error
        """
        try:
            # Calculate frames
            silence_frames = int(silence_duration * self.sample_rate)
            min_frames = int(min_duration * self.sample_rate)
            max_frames = int(duration * self.sample_rate)
            
            # Record audio
            recording = sd.rec(
                max_frames,
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32'
            )
            
            # Wait for recording to complete or detect silence
            frames_recorded = 0
            silence_count = 0
            check_interval_ms = 200  # Check every 200ms (less frequent, more stable)
            check_interval_frames = int(check_interval_ms / 1000.0 * self.sample_rate)
            
            while frames_recorded < max_frames:
                sd.wait(check_interval_ms)
                frames_recorded += check_interval_frames
                
                # Don't stop before minimum duration
                if frames_recorded < min_frames:
                    silence_count = 0  # Reset silence counter during min duration
                    continue
                
                if frames_recorded >= max_frames:
                    break
                
                # Check for silence in a larger window (more stable)
                window_size = min(check_interval_frames * 2, frames_recorded)
                chunk = recording[max(0, frames_recorded - window_size):frames_recorded]
                
                # Use RMS (root mean square) for better silence detection
                rms = np.sqrt(np.mean(chunk**2))
                
                if rms < silence_threshold:
                    silence_count += check_interval_frames
                    if silence_count >= silence_frames:
                        # Stop recording on silence (but only after min duration)
                        sd.stop()
                        recording = recording[:frames_recorded]
                        break
                else:
                    silence_count = 0  # Reset if we detect sound
            
            sd.wait()  # Ensure recording is complete
            
            # Trim to actual recorded length
            if frames_recorded < max_frames:
                recording = recording[:frames_recorded]
            
            return recording
            
        except Exception as e:
            print(f"Recording error: {e}")
            return None
    
    def transcribe_audio(self, audio_data: np.ndarray) -> str:
        """
        Transcribe audio data to text.
        
        Args:
            audio_data: Audio as numpy array
            
        Returns:
            Transcribed text
        """
        try:
            # Flatten audio if needed
            if audio_data.ndim > 1:
                audio_data = audio_data.flatten()
            
            # Transcribe with better settings
            segments, info = self.model.transcribe(
                audio_data,
                beam_size=5,
                language="en",
                vad_filter=True,  # Voice activity detection
                word_timestamps=False,
                condition_on_previous_text=True,  # Better context
            )
            
            # Combine segments
            text = " ".join([segment.text for segment in segments])
            text = text.strip()
            
            if text:
                print(f"✓ Transcribed: '{text}'")
            else:
                print("⚠️  No speech detected in audio")
            
            return text
            
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
    
    def listen(
        self,
        duration: int = 5,
        silence_threshold: float = 0.01,
        silence_duration: float = 1.5,
        min_duration: float = 1.0
    ) -> str:
        """
        Record and transcribe in one step.
        
        Args:
            duration: Maximum recording duration
            silence_threshold: Silence detection threshold
            silence_duration: Seconds of silence before stopping
            min_duration: Minimum recording duration
            
        Returns:
            Transcribed text
        """
        audio = self.record_audio(duration, silence_threshold, silence_duration, min_duration)
        if audio is not None:
            return self.transcribe_audio(audio)
        return ""
    
    def transcribe_file(self, audio_path: str) -> str:
        """
        Transcribe audio from file.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        try:
            segments, info = self.model.transcribe(audio_path, beam_size=5)
            text = " ".join([segment.text for segment in segments])
            return text.strip()
        except Exception as e:
            print(f"File transcription error: {e}")
            return ""


if __name__ == "__main__":
    # Test STT
    print("Testing Speech-to-Text...")
    stt = SpeechToText(model_size="base")
    
    print("\nSpeak something (5 seconds)...")
    text = stt.listen(duration=5)
    print(f"\nYou said: '{text}'")

