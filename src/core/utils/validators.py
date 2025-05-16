"""Input validation utilities for BeAnonymous."""

class Validators:
    """Input validation utility class."""
    
    @staticmethod
    def validate_script(script: str) -> bool:
        """Validate the input script.
        
        Args:
            script (str): The script to validate
            
        Returns:
            bool: True if script is valid
        """
        return bool(script and script.strip())
    
    @staticmethod
    def validate_video_name(video_name: str, available_videos: list) -> bool:
        """Validate video selection.
        
        Args:
            video_name (str): Selected video name
            available_videos (list): List of available videos
            
        Returns:
            bool: True if video selection is valid
        """
        return video_name in available_videos
    
    @staticmethod
    def validate_audio_name(audio_name: str, available_audio: list) -> bool:
        """Validate audio selection.
        
        Args:
            audio_name (str): Selected audio name
            available_audio (list): List of available audio files
            
        Returns:
            bool: True if audio selection is valid
        """
        return audio_name in available_audio
