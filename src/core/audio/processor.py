"""Audio processing utilities for BeAnonymous."""

import subprocess
import os
from pathlib import Path
from ...config.settings import TEMP_PATH

class AudioProcessor:
    """Audio processing class for manipulating generated TTS audio."""
    
    @staticmethod
    def convert_pitch(input_path=None, 
                     output_path=None,
                     pitch_factor=0.8):
        """Convert the pitch of an audio file using ffmpeg."""
        try:
            # Create temp directory if it doesn't exist
            TEMP_PATH.mkdir(parents=True, exist_ok=True)

            # Use default paths if none provided, ensure they are absolute
            if input_path is None:
                input_path = TEMP_PATH.resolve() / "normal_audio.mp3"
            if output_path is None:
                output_path = TEMP_PATH.resolve() / "final_tts.mp3"
            
            # Ensure paths are Path objects and absolute
            input_path = Path(input_path).resolve()
            output_path = Path(output_path).resolve()
            
            print(f" [AUDIO PROCESSOR] Using input path: {input_path}")
            print(f" [AUDIO PROCESSOR] Using output path: {output_path}")
            
            # Verify the input file exists
            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")

            # FFMPEG command with proper path handling
            cmd = f'ffmpeg -y -i "{input_path}" -af "asetrate=44100*{pitch_factor},aresample=44100" -ar 44100 "{output_path}"'
            
            subprocess.run(cmd, check=True, capture_output=True, shell=True)
            print(" [AUDIO PROCESSOR] Success: Pitch conversion completed")
            return True
            
        except subprocess.CalledProcessError as e:
            print(" [AUDIO PROCESSOR] Error: FFMPEG command failed")
            print(e.stderr.decode())
            return False
        except Exception as e:
            print(" [AUDIO PROCESSOR] Error: Pitch conversion failed")
            print(e)
            return False