"""Video generation module for BeAnonymous."""

import subprocess
import os
from pathlib import Path
from typing import Optional, Callable
from ...config.settings import (
    VIDEO_ASSETS_PATH, 
    AUDIO_ASSETS_PATH,
    INTRO_VIDEO_PATH,
    VIDEO_OUTPUT_FILENAME,
    TEMP_PATH,
    RESOURCES_DIR
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
        self.video_path = Path(VIDEO_ASSETS_PATH) / f"{video_name}.mp4"
        self.audio_path = Path(AUDIO_ASSETS_PATH) / f"{audio_name}.mp3"
        self.output_path = Path(output_path)
        self.add_intro = add_intro
        self.tts_path = TEMP_PATH / "final_tts.mp3"
        
        # If video file doesn't exist in new stock directory, try alternative locations
        if not self.video_path.exists():
            # Try to find the video in the resources/videos directory as a fallback
            fallback_path = RESOURCES_DIR / "videos" / f"{video_name}.mp4"
            if fallback_path.exists():
                self.video_path = fallback_path
                print(f" [VIDEO GENERATOR] Using fallback video path: {self.video_path}")
            else:
                print(f" [VIDEO GENERATOR] Video file not found: {self.video_path}")
                raise FileNotFoundError(f"Video file not found: {self.video_path}")
        
        # Ensure other required files exist
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

    def _get_video_duration(self, video_path):
        """Get duration of video file using ffprobe.
        
        Args:
            video_path (str): Path to video file
            
        Returns:
            float: Duration in seconds
        """
        try:
            cmd = f'ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{video_path}"'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            return float(result.stdout.strip())
        except Exception as e:
            print(f" [VIDEO GENERATOR] Error getting video duration: {str(e)}")
            raise

    def generate(self, progress_callback: Optional[Callable[[float], None]] = None) -> bool:
        """Generate the final video using FFmpeg stream copying.
        
        Args:
            progress_callback: Optional callback function to receive progress updates
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if progress_callback:
                progress_callback(0)  # Start progress
                
            # Get TTS audio duration
            tts_duration = self._get_audio_duration(self.tts_path)
            if progress_callback:
                progress_callback(10)  # Get audio duration done
            
            # Prepare output path
            output_file = self.output_path / VIDEO_OUTPUT_FILENAME
            temp_video = TEMP_PATH / "temp_video.mp4"

            if self.add_intro:
                # Get intro video duration
                intro_duration = self._get_video_duration(INTRO_VIDEO_PATH)
                if progress_callback:
                    progress_callback(20)  # Get video duration done
                
                # First create a temporary concatenated video
                concat_file = TEMP_PATH / "concat.txt"
                with open(concat_file, 'w') as f:
                    f.write(f"file '{INTRO_VIDEO_PATH}'\n")
                    f.write(f"file '{self.video_path}'\n")
                
                if progress_callback:
                    progress_callback(30)  # Concat file created
                
                # First concatenate the videos
                concat_cmd = [
                    'ffmpeg', '-y',
                    '-hide_banner', '-loglevel', 'warning',
                    '-f', 'concat', '-safe', '0', 
                    '-i', str(concat_file),
                    '-c', 'copy',
                    str(temp_video)
                ]
                subprocess.run(concat_cmd, check=True)
                
                if progress_callback:
                    progress_callback(50)  # Video concatenation done
                
                # Now add the audio with proper timing
                cmd = [
                    'ffmpeg', '-y',
                    '-hide_banner', '-loglevel', 'warning',
                    '-i', str(temp_video),  # Input concatenated video
                    '-i', str(self.tts_path),  # TTS audio
                    '-i', str(self.audio_path),  # Background audio
                    '-filter_complex',
                    # Delay TTS to start after intro, mix with background audio
                    f'[1:a]adelay={int(intro_duration*1000)}|{int(intro_duration*1000)}[delayed_tts];'
                    '[delayed_tts][2:a]amix=inputs=2:duration=first[a]',
                    '-map', '0:v', '-map', '[a]',
                    # Trim to intro duration plus TTS duration
                    '-t', str(intro_duration + tts_duration),
                    '-c:v', 'copy',
                    str(output_file)
                ]
            else:
                # Without intro, simpler command
                cmd = [
                    'ffmpeg', '-y',
                    '-hide_banner', '-loglevel', 'warning',
                    '-stream_loop', '-1',  # Loop input video
                    '-t', str(tts_duration),  # Duration from TTS
                    '-i', str(self.video_path),  # Input video
                    '-i', str(self.tts_path),  # TTS audio
                    '-i', str(self.audio_path),  # Background audio
                    '-filter_complex', '[1:a][2:a]amix=inputs=2:duration=first[a]',
                    '-map', '0:v', '-map', '[a]',
                    '-c:v', 'copy',  # Copy video stream without re-encoding
                    str(output_file)
                ]
            
            if progress_callback:
                progress_callback(70)  # FFmpeg command prepared
            
            # Run FFmpeg command
            subprocess.run(cmd, check=True)
            if progress_callback:
                progress_callback(90)  # FFmpeg processing done
            
            print(f" [VIDEO GENERATOR] Success: Video generated at {output_file}")
            
            # Clean up temporary files
            if self.add_intro:
                if concat_file.exists():
                    concat_file.unlink()
                if temp_video.exists():
                    temp_video.unlink()
                    
            if progress_callback:
                progress_callback(100)  # All done
                
            return True
            
        except subprocess.CalledProcessError as e:
            print(f" [VIDEO GENERATOR] FFmpeg Error: {e.stderr.decode() if e.stderr else str(e)}")
            return False
        except Exception as e:
            print(f" [VIDEO GENERATOR] Error: {str(e)}")
            return False
