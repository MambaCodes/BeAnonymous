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
        Uses the classic hacker-style low pitch effect while maintaining speed.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
            
            # FFMPEG command to create a low-pitched, hacker-style voice effect
            # The command uses the following audio filter chain:
            # - asetrate=44100*0.35: Reduces the sample rate to 35% which lowers the pitch
            # - aresample=44100: Resamples back to standard 44.1kHz for compatibility
            # Note: This method provides a clean pitch shift while maintaining audio quality

            cmd = f"ffmpeg -y -i {str(self.temp_path)} -af asetrate=44100*0.35,aresample=44100 {str(self.output_path)}"
            print(f" [TTS GENERATOR] Executing FFmpeg command: {cmd}")
            try:
                result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
                print(f" [TTS GENERATOR] FFmpeg stdout: {result.stdout}")
                print(f" [TTS GENERATOR] FFmpeg stderr: {result.stderr}")
            except subprocess.CalledProcessError as e:
                print(f" [TTS GENERATOR] FFmpeg command failed with error: {e.stderr}")
                return False

            if os.path.exists(str(self.output_path)):
                print(f" [TTS GENERATOR] Output file created successfully at: {self.output_path}")
                # Verify the output file size
                if os.path.getsize(str(self.output_path)) > 0:
                    # Clean up the temporary normal audio file
                    try:
                        if self.temp_path.exists():
                            self.temp_path.unlink()
                            print(f" [TTS GENERATOR] Cleaned up temporary file: {self.temp_path}")
                    except Exception as e:
                        print(f" [TTS GENERATOR] Warning: Could not delete temporary file: {e}")
                    return True
                else:
                    print(" [TTS GENERATOR] Warning: Output file was created but is empty")
                    return False
            else:
                print(f" [TTS GENERATOR] Warning: Output file not found at: {self.output_path}")
                return False
            
        except subprocess.CalledProcessError as e:
            print(" [TTS GENERATOR] Error: FFMPEG command failed")
            print(f" [TTS GENERATOR] Error details: {e.stderr.decode()}")
            return False
        except Exception as error:
            print(" [TTS GENERATOR] Error: Pitch adjustment failed")
            print(f" [TTS GENERATOR] Error details: {str(error)}")
            return False
    
    def generate(self):
        """Generate TTS audio file with pitch adjustment.
        
        Returns:
            bool: True if successful, False otherwise
        """
        print("\n=== Starting TTS Generation Process ===")
        
        # First generate the initial TTS
        print(" [TTS GENERATOR] Step 1: Generating initial TTS...")
        if not self._generate_tts():
            print(" [TTS GENERATOR] Failed to generate initial TTS")
            return False
        
        print(f" [TTS GENERATOR] Initial TTS file exists: {self.temp_path.exists()}")
        if self.temp_path.exists():
            print(f" [TTS GENERATOR] Initial TTS file size: {self.temp_path.stat().st_size} bytes")
            
        # Then adjust the pitch
        print("\n [TTS GENERATOR] Step 2: Adjusting pitch...")
        if not self._adjust_pitch():
            print(" [TTS GENERATOR] Failed to adjust pitch")
            return False
            
        print(f" [TTS GENERATOR] Output file exists: {self.output_path.exists()}")
        if self.output_path.exists():
            print(f" [TTS GENERATOR] Output file size: {self.output_path.stat().st_size} bytes")
        
        print("=== TTS Generation Process Complete ===\n")
        return True
