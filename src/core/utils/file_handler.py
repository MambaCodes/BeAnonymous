"""File handling utilities for BeAnonymous."""

import os
import shutil
from pathlib import Path
from typing import List, Optional
from ...config.settings import VIDEO_ASSETS_PATH, AUDIO_ASSETS_PATH

class FileHandler:
    """File handling utility class."""
    
    @staticmethod
    def ensure_directory_exists(directory: str) -> None:
        """Create directory if it doesn't exist.
        
        Args:
            directory (str): Directory path to create
        """
        os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def get_video_files() -> List[str]:
        """Get list of available background videos.
        
        Returns:
            List[str]: List of video filenames without extension
        """
        videos = []
        try:
            if VIDEO_ASSETS_PATH.exists():
                for file in os.listdir(VIDEO_ASSETS_PATH):
                    if file.endswith(".mp4"):
                        videos.append(os.path.splitext(file)[0])
            
            if not videos:
                print(" [FILE HANDLER] No videos found in stock directory")
                # Return empty list instead of ["Default"]
                return []
                
            return videos
        except Exception as e:
            print(f" [FILE HANDLER] Error reading video directory: {e}")
            return []  # Return empty list on error
    
    @staticmethod
    def get_audio_files() -> List[str]:
        """Get list of available background music.
        
        Returns:
            List[str]: List of audio filenames without extension
        """
        music = []
        for file in os.listdir(AUDIO_ASSETS_PATH):
            if file.endswith(".mp3"):
                music.append(os.path.splitext(file)[0])
        return music or ["Default"]
    
    @staticmethod
    def validate_output_path(path: str) -> bool:
        """Validate if output path exists and is writable.
        
        Args:
            path (str): Path to validate
            
        Returns:
            bool: True if path is valid
        """
        try:
            if not path:
                return False
            
            directory = Path(path)
            if not directory.exists():
                return False
                
            # Try creating a test file to verify write permissions
            test_file = directory / ".write_test"
            test_file.touch()
            test_file.unlink()
            
            return True
            
        except (OSError, PermissionError):
            return False
