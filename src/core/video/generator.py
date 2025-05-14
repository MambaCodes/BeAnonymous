"""Video generation module for BeAnonymous."""

import subprocess
import os
from pathlib import Path
from ...config.settings import (
    VIDEO_ASSETS_PATH, 
    AUDIO_ASSETS_PATH,
    INTRO_VIDEO_PATH,
    VIDEO_OUTPUT_FILENAME,
    TEMP_PATH 
)

class VideoGenerator:
    """Video generator class for creating anonymous videos."""
    def __init__(self, video_name, audio_name, output_path, add_intro=False):
        """Initialize video generator.
        
        Args:
            video_name (str): Name of the background video file (without extension)
            audio_name (str): Name of the background audio file (without extension)
            output_path (str): Directory to save the final video
            add_intro (bool): Whether to add the anonymous intro
        """
        # Convert paths to Path objects for better path handling
        self.video_path = Path(VIDEO_ASSETS_PATH) / f"{video_name}.mp4"
        self.audio_path = Path(AUDIO_ASSETS_PATH) / f"{audio_name}.mp3"
        self.output_path = Path(output_path)
        self.add_intro = add_intro
        self.tts_path = TEMP_PATH / "final_tts.mp3"

        # Ensure all required files exist
        if not self.video_path.exists():
            raise FileNotFoundError(f"Video file not found: {self.video_path}")
        if not self.audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {self.audio_path}")
        if not self.tts_path.exists():
            raise FileNotFoundError(f"TTS audio file not found: {self.tts_path}")
        if add_intro and not Path(INTRO_VIDEO_PATH).exists():
            raise FileNotFoundError(f"Intro video not found: {INTRO_VIDEO_PATH}")

    def _get_audio_duration(self, audio_path):
        """Get duration of audio file using ffprobe.
        
        Args:
            audio_path (str): Path to audio file
            
        Returns:
            float: Duration in seconds
        """
        try:
            cmd = f'ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{audio_path}"'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            return float(result.stdout.strip())
        except Exception as e:
            print(f" [VIDEO GENERATOR] Error getting audio duration: {str(e)}")
            raise

    def generate(self):
        """Generate the final video using FFmpeg stream copying.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get TTS audio duration
            tts_duration = self._get_audio_duration(self.tts_path)
            
            # Prepare output path
            output_file = self.output_path / VIDEO_OUTPUT_FILENAME
            
            # Prepare FFmpeg command
            if self.add_intro:
                # If adding intro, we need to concatenate videos
                # First create a temporary file list
                concat_file = TEMP_PATH / "concat.txt"
                with open(concat_file, 'w') as f:
                    f.write(f"file '{INTRO_VIDEO_PATH}'\n")
                    f.write(f"file '{self.video_path}'\n")
                
                # FFmpeg command for concatenating videos and adding audio
                cmd = [
                    'ffmpeg', '-y',
                    '-hide_banner', '-loglevel', 'warning',
                    '-f', 'concat', '-safe', '0', '-i', str(concat_file),
                    '-stream_loop', '-1', # Loop the concatenated video
                    '-t', str(tts_duration), # Trim to TTS duration
                    '-i', str(self.tts_path), # TTS audio
                    '-i', str(self.audio_path), # Background audio
                    '-filter_complex', f'[1:a][2:a]amix=inputs=2:duration=first[a]',
                    '-map', '0:v', '-map', '[a]',
                    '-c:v', 'copy', # Copy video stream without re-encoding
                    str(output_file)
                ]
            else:
                # Without intro, simpler command
                cmd = [
                    'ffmpeg', '-y',
                    '-hide_banner', '-loglevel', 'warning',
                    '-stream_loop', '-1', # Loop input video
                    '-t', str(tts_duration), # Duration from TTS
                    '-i', str(self.video_path), # Input video
                    '-i', str(self.tts_path), # TTS audio
                    '-i', str(self.audio_path), # Background audio
                    '-filter_complex', f'[1:a][2:a]amix=inputs=2:duration=first[a]',
                    '-map', '0:v', '-map', '[a]',
                    '-c:v', 'copy', # Copy video stream without re-encoding
                    str(output_file)
                ]
            
            # Run FFmpeg command
            subprocess.run(cmd, check=True)
            print(f" [VIDEO GENERATOR] Success: Video generated at {output_file}")
            
            # Clean up concat file if it was created
            if self.add_intro and concat_file.exists():
                concat_file.unlink()
                
            return True
            
        except subprocess.CalledProcessError as e:
            print(f" [VIDEO GENERATOR] FFmpeg Error: {e.stderr.decode() if e.stderr else str(e)}")
            return False
        except Exception as e:
            print(f" [VIDEO GENERATOR] Error: {str(e)}")
            return False
