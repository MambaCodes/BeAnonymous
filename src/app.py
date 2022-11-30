from tts.tts_generator import TTS
from tts.converter import Converter

from video.video_generator import GenerateVideo

user_input=input("\n>> ")

# Text Audio Generation
engine=TTS(user_input)
engine.generate()
converter=Converter()
converter.convert_pitch()
# Output Received --> final_audio.mp3 (in temp folder)



# Video Generation
video=GenerateVideo("new","aud_1")
