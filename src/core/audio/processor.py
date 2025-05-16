"""Audio processing utilities for BeAnonymous."""

import subprocess
from pathlib import Path
from ...config.settings import TEMP_PATH
from ..utils.logger import get_logger
from ..utils.settings_manager import SettingsManager

logger = get_logger('AUDIO')

class AudioProcessor:
    """Audio processing class for manipulating generated TTS audio."""
    
    @staticmethod    
    def convert_pitch(input_path=None, 
                     output_path=None):
        """Convert the pitch of an audio file using ffmpeg."""
        settings = SettingsManager.load_settings()
        pitch_factor = settings.get('pitch_factor', 0.35)
        """Convert the pitch of an audio file using ffmpeg."""
        try:
            # Create temp directory if it doesn't exist
            TEMP_PATH.mkdir(parents=True, exist_ok=True)

            # Ensure paths are Path objects and absolute
            input_path = Path(input_path).resolve()
            output_path = Path(output_path).resolve()
            
            logger.info(f"Using input path: {input_path}")
            logger.info(f"Using output path: {output_path}")
            
            # Verify the input file exists
            if not input_path.exists():
                logger.error(f"Input file not found: {input_path}")
                raise FileNotFoundError(f"Input file not found: {input_path}")

            # FFMPEG command to create a low-pitched, hacker-style voice effect
            cmd = [
                'ffmpeg', '-y',
                '-hide_banner', '-loglevel', 'warning',
                '-i', str(input_path),
                '-af', f'asetrate=44100*{pitch_factor},aresample=44100',
                str(output_path)
            ]
            
            logger.info("Processing audio pitch adjustment...")
            subprocess.run(cmd, check=True)
            logger.info(f"Output file created at: {output_path}")
            input_path.unlink()  # Remove the original file after processing
            logger.info(f"Originally generated tts file {input_path} deleted")
            logger.info("Audio pitch adjustment completed")
            
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg Error: {e.stderr.decode() if e.stderr else str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            raise