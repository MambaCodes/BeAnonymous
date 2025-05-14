"""Text-to-speech generator for BeAnonymous."""

import os
import pyttsx3
import subprocess
from ...config.settings import TTS_RATE, TTS_VOICE_ID, TEMP_PATH
from pathlib import Path

class TTS:
    """Text-to-speech generator class with pitch adjustment capabilities."""
    
    def __init__(self, text, output_path=None):
        """Initialize TTS generator.
        
        Args:
            text (str): Text to convert to speech
            output_path (str, optional): Path to save the final processed audio file
        """
        self.text = text

        # Create temp directory if it doesn't exist
        TEMP_PATH.mkdir(parents=True, exist_ok=True)

        # Setup paths using pathlib and make them absolute 
        self.temp_path = TEMP_PATH.resolve() / "normal_audio.mp3"
        self.output_path = TEMP_PATH.resolve() / "final_tts.mp3" if output_path is None else Path(output_path).resolve()
        
        print(f" [TTS GENERATOR] Using temp path: {self.temp_path}")
        print(f" [TTS GENERATOR] Using output path: {self.output_path}")
        
        self._init_engine()
    
    def _init_engine(self):
        """Initialize the TTS engine with default settings."""
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[TTS_VOICE_ID].id)
        self.engine.setProperty('rate', TTS_RATE)
    
    def _generate_tts(self):
        """Generate initial TTS audio file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print(f" [TTS GENERATOR] Attempting to save TTS to: {self.temp_path}")
            print(f" [TTS GENERATOR] Text to convert: {self.text[:100]}...")  # First 100 chars
            print(f" [TTS GENERATOR] Temp path exists: {self.temp_path.parent.exists()}")
            
            # Create parent directory if it doesn't exist
            self.temp_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get absolute path
            abs_temp_path = str(self.temp_path.resolve())
            print(f" [TTS GENERATOR] Using absolute path: {abs_temp_path}")
            
            # Save the file
            self.engine.save_to_file(self.text, abs_temp_path)
            self.engine.runAndWait()
            
            # Verify file was created
            if self.temp_path.exists():
                print(f" [TTS GENERATOR] Success: TTS file was created at {self.temp_path}")
                return True
            else:
                print(f" [TTS GENERATOR] Error: TTS file was not created at {self.temp_path}")
                return False
                
        except Exception as error:
            print(" [TTS GENERATOR] Failure: TTS generation failed")
            print(f" [TTS GENERATOR] Error details: {str(error)}")
            print(f" [TTS GENERATOR] Error type: {type(error)}")
            return False
    
    def _adjust_pitch(self):
        """Convert the pitch of the generated audio file using ffmpeg.
        Uses the classic hacker-style low pitch effect.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            
            # FFMPEG command to adjust pitch to low, hacker-style voice (rate=0.35)
            cmd = f'ffmpeg -y -i "{self.temp_path}" -af "asetrate=44100*0.35,aresample=44100" -ar 44100 "{self.output_path}"'
            subprocess.run(cmd, check=True, capture_output=True, shell=True)
            
            # Clean up temporary file
            # if os.path.exists(self.temp_path):
            #     os.remove(self.temp_path)
                
            print(" [TTS GENERATOR] Success: Pitch adjustment completed")
            return True
            
        except subprocess.CalledProcessError as e:
            print(" [TTS GENERATOR] Error: FFMPEG command failed")
            print(e.stderr.decode())
            return False
        except Exception as error:
            print(" [TTS GENERATOR] Error: Pitch adjustment failed")
            print(error)
            return False
    
    def generate(self):
        """Generate TTS audio file with pitch adjustment.
        
        Returns:
            bool: True if successful, False otherwise
        """
        # First generate the initial TTS
        if not self._generate_tts():
            return False
            
        # Then adjust the pitch
        if not self._adjust_pitch():
            return False
            
        return True
