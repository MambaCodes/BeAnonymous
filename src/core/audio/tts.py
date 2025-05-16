"""Text-to-speech generator for BeAnonymous."""

import os
import pyttsx3
import subprocess
from ...config.settings import TTS_RATE, TTS_VOICE_ID, TEMP_PATH
from pathlib import Path
from ..utils.logger import get_logger

logger = get_logger('TTS')

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
        
        logger.info(f"Using temp path: {self.temp_path}")
        logger.info(f"Using output path: {self.output_path}")
        
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
            logger.info("Generating TTS audio...")
            logger.info(f"Attempting to save TTS to: {self.temp_path}")
            logger.info(f"Text to convert: {self.text[:100]}...")  # First 100 chars
            logger.info(f"Temp path exists: {self.temp_path.parent.exists()}")
            
            # Create parent directory if it doesn't exist
            self.temp_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Get absolute path
            abs_temp_path = str(self.temp_path.resolve())
            logger.info(f"Using absolute path: {abs_temp_path}")
            
            # Save the file
            self.engine.save_to_file(self.text, abs_temp_path)
            self.engine.runAndWait()
            
            # Verify file was created
            if self.temp_path.exists():
                logger.info(f"Success: TTS file was created at {self.temp_path}")
                return True
            else:
                logger.error(f"Error: TTS file was not created at {self.temp_path}")
                return False
                
        except Exception as error:
            logger.error(f"TTS generation failed: {str(error)}")
            return False
    
    def _adjust_pitch(self):
        """Convert the pitch of the generated audio file using ffmpeg.
        Uses the classic hacker-style low pitch effect while maintaining speed.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Adjusting audio pitch...")
            from ..audio.processor import AudioProcessor
            AudioProcessor.convert_pitch(self.temp_path, self.output_path)
            return True
        except Exception as e:
            logger.error(f"Pitch adjustment failed: {str(e)}")
            return False
    
    def generate(self):
        """Generate TTS audio file with pitch adjustment.
        
        Returns:
            bool: True if successful, False otherwise
        """
        logger.info("=== Starting TTS Generation Process ===")
        
        # First generate the initial TTS
        logger.info("Generating initial TTS...")
        if not self._generate_tts():
            logger.error("Failed to generate initial TTS")
            return False
        
        logger.info(f"Initial TTS file exists: {self.temp_path.exists()}")
        if self.temp_path.exists():
            logger.info(f"Initial TTS file size: {self.temp_path.stat().st_size} bytes")
            
        # Then adjust the pitch
        logger.info("Adjusting pitch...")
        if not self._adjust_pitch():
            logger.error("Failed to adjust pitch")
            return False
            
        logger.info(f"Output file exists: {self.output_path.exists()}")
        if self.output_path.exists():
            logger.info(f"Output file size: {self.output_path.stat().st_size} bytes")
        
        logger.info("TTS Generation Process Complete")
        return True
