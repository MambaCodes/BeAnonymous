# This File is For Testing how this Video generator Works :
from tts.tts_generator import TTS
from tts.converter import Converter
from video.video_generator import GenerateVideo



user_input=input("Enter Script for Video :\n>> ")



# Text Audio Generation
engine=TTS(user_input)
engine.generate()
converter=Converter()
converter.convert_pitch()
# Output Received --> final_audio.mp3 (in temp folder)

# Video Generation (Asking for Required Parameters)
path=input("Enter Path for Output File :\n>>")
intro=input("Do you Want Anonymous Intro in the video (y/n) -> ")
if intro.lower()=="y":
    intro=True
else:
    intro=False

# Generating Video
video=GenerateVideo("Default","Default",path,intro)
# Here "Default","Default" is the Default Sample Video,Background Song.