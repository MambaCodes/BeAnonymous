"""Video editing utilities for BeAnonymous."""

from moviepy.editor import TextClip, CompositeVideoClip
from typing import Optional

class VideoEditor:
    """Video editing utilities class."""
    
    @staticmethod
    def add_subtitles(video_clip, text: str, font_size: int = 30,
                    color: str = 'white', duration: Optional[float] = None):
        """Add subtitles to a video clip.
        
        Args:
            video_clip: MoviePy video clip
            text (str): Subtitle text
            font_size (int): Font size for subtitles
            color (str): Font color for subtitles
            duration (float, optional): Duration for subtitles
            
        Returns:
            CompositeVideoClip: Video with subtitles
        """
        txt_clip = TextClip(text, fontsize=font_size, color=color)
        
        if duration:
            txt_clip = txt_clip.set_duration(duration)
        else:
            txt_clip = txt_clip.set_duration(video_clip.duration)
            
        txt_clip = txt_clip.set_position(('center', 'bottom'))
        
        return CompositeVideoClip([video_clip, txt_clip])
