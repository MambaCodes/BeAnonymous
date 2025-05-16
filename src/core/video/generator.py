"""Video generation module for BeAnonymous."""

import subprocess
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
from ..utils.logger import get_logger

logger = get_logger('GENERATOR')

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
                logger.info(f"Using fallback video path: {self.video_path}")
            else:
                logger.error(f"Video file not found: {self.video_path}")
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
            logger.error(f"Error getting audio duration: {str(e)}")
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
            logger.error(f"Error getting video duration: {str(e)}")
            raise    
        
    def generate(self, progress_callback: Optional[Callable[[float], None]] = None) -> bool:
        """Generate the final video using FFmpeg stream copying.
        
        Args:
            progress_callback: Optional callback function to receive progress updates
            
        Returns:
            bool: True if successful, False otherwise
        """
        temp_files = []  # Keep track of all temp files
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
            temp_audio = TEMP_PATH / "temp_audio.mp3"
            
            # Add temp files to tracking list
            temp_files.extend([temp_video, temp_audio])

            if self.add_intro:
                # Get intro video duration
                intro_duration = self._get_video_duration(INTRO_VIDEO_PATH)
                if progress_callback:
                    progress_callback(20)  # Get video duration done
                
                # First create mixed audio for main video section (TTS + background music)
                audio_mix_cmd = [
                    'ffmpeg', '-y',
                    '-hide_banner', '-loglevel', 'warning',
                    '-i', str(self.tts_path),  # TTS audio
                    '-i', str(self.audio_path),  # Background audio
                    '-filter_complex', '[0:a][1:a]amix=inputs=2:duration=first[a]',
                    '-map', '[a]',
                    str(temp_audio)
                ]
                subprocess.run(audio_mix_cmd, check=True)
                
                if progress_callback:
                    progress_callback(30)  # Audio mix done
                
                # Now create a temporary video with the mixed audio
                temp_main_cmd = [
                    'ffmpeg', '-y',
                    '-hide_banner', '-loglevel', 'warning',
                    '-stream_loop', '-1',  # Loop input video
                    '-t', str(tts_duration),  # Duration from TTS
                    '-i', str(self.video_path),  # Input video
                    '-i', str(temp_audio),  # Mixed audio
                    '-map', '0:v',  # Take video from first input
                    '-map', '1:a',  # Take audio from second input
                    str(temp_video)  # Don't use -c:v copy here to ensure compatibility
                ]
                subprocess.run(temp_main_cmd, check=True)
                
                if progress_callback:
                    progress_callback(50)  # Temp video created
                
                # Finally concatenate intro and main video ensuring format compatibility
                concat_cmd = [
                    'ffmpeg', '-y',
                    '-hide_banner', '-loglevel', 'warning',
                    '-i', str(INTRO_VIDEO_PATH),  # First input - intro
                    '-i', str(temp_video),  # Second input - main video
                    '-filter_complex',
                    '[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[outv][outa]',  # Proper concatenation
                    '-map', '[outv]',  # Map concatenated video
                    '-map', '[outa]',  # Map concatenated audio
                    str(output_file)
                ]
                subprocess.run(concat_cmd, check=True)
                
            else:
                try:
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
                        str(output_file)
                    ]
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as e:
                    logger.error(f"FFmpeg Error: {e.stderr.decode() if e.stderr else str(e)}")
                    if output_file.exists():
                        output_file.unlink()  # Delete failed output file
                    raise
            
            if progress_callback:
                progress_callback(90)  # FFmpeg processing done
            
            logger.info(f"Success: Video generated at {output_file}")
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            # Clean up any partially created output file
            if output_file.exists():
                try:
                    output_file.unlink()
                except:
                    pass
            return False
            
        finally:
            # Clean up ALL temporary files
            try:
                # Clean up temp files 
                for temp_file in temp_files:
                    if temp_file.exists():
                        try:
                            temp_file.unlink()
                            logger.info(f"Cleaned up temp file: {temp_file}")
                        except Exception as e:
                            logger.error(f"Failed to clean up {temp_file}: {e}")
                
                # Clean up TTS file after generation
                if self.tts_path.exists():
                    try:
                        self.tts_path.unlink()
                        logger.info("Cleaned up TTS file")
                    except Exception as e:
                        logger.error(f"Failed to clean up TTS file: {e}")
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")
                
            if progress_callback:
                progress_callback(100)  # All done
            
        return True
