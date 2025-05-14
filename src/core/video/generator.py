"""Video generation module for BeAnonymous."""

from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, concatenate_audioclips
import os
import os
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
        self.video_path = os.path.join(VIDEO_ASSETS_PATH, f"{video_name}.mp4")
        self.audio_path = os.path.join(AUDIO_ASSETS_PATH, f"{audio_name}.mp3")
        self.output_path = output_path
        self.add_intro = add_intro
        temp_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "utils", "temp")
        self.tts_path = os.path.join(TEMP_PATH, "final_tts.mp3")

    def _load_media(self):
        """Load all required media files."""
        self.tts_audio = AudioFileClip(self.tts_path)
        self.stock_clip = VideoFileClip(self.video_path)
        self.stock_bg = AudioFileClip(self.audio_path)
        if self.add_intro:
            self.intro_clip = VideoFileClip(INTRO_VIDEO_PATH)

    def _process_background_audio(self):
        """Process and prepare background music."""
        if self.stock_bg.duration < self.tts_audio.duration:
            while self.stock_bg.duration < self.tts_audio.duration:
                self.stock_bg = concatenate_audioclips([self.stock_bg, self.stock_bg])
        self.stock_bg = self.stock_bg.set_duration(self.tts_audio.duration)

    def _process_video(self):
        """Process and prepare video clip."""
        if self.stock_clip.duration < self.tts_audio.duration:
            while self.stock_clip.duration < self.tts_audio.duration:
                self.stock_clip = concatenate_videoclips([self.stock_clip, self.stock_clip])
        self.stock_clip = self.stock_clip.set_duration(self.tts_audio.duration)

    def generate(self):
        """Generate the final video.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load all media files
            self._load_media()
            
            # Process background audio
            self._process_background_audio()
            
            # Create composite audio
            final_audio = CompositeAudioClip([self.tts_audio, self.stock_bg])
            
            # Process and prepare video
            self._process_video()
            final_video = self.stock_clip.set_audio(final_audio)
            
            # Add intro if requested
            if self.add_intro:
                final_video = concatenate_videoclips([self.intro_clip, final_video])
            
            # Ensure output path ends with separator
            if not (self.output_path.endswith('/') or self.output_path.endswith('\\\\')):
                self.output_path += '/'
                
            # Generate final video
            output_file = self.output_path + VIDEO_OUTPUT_FILENAME
            final_video.write_videofile(output_file)
            
            return True
            
        except Exception as e:
            print(" [VIDEO GENERATOR] Error: Video generation failed")
            print(e)
            return False
        finally:
            # Clean up loaded clips
            if hasattr(self, 'tts_audio'):
                self.tts_audio.close()
            if hasattr(self, 'stock_clip'):
                self.stock_clip.close()
            if hasattr(self, 'stock_bg'):
                self.stock_bg.close()
            if hasattr(self, 'intro_clip'):
                self.intro_clip.close()
