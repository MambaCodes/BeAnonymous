from moviepy.editor import *



def generate_video(SampleVideo,AudioBackground,Path,add_intro,video_script):
    ttsaudio=AudioFileClip("src/temp/final_tts.mp3")
    stockclip=VideoFileClip("src/video/assets/" + SampleVideo + ".mp4")
    stockbg=AudioFileClip("src/video/assets/" + AudioBackground + ".mp3")
    anon_intro=VideoFileClip("src/video/assets/intro/anon_intro.mp4")
    #Genetraing Background Audio
    if (stockbg.duration < ttsaudio.duration):
        while (stockbg.duration < ttsaudio.duration):
            final_bg=concatenate_audioclips([stockbg,stockbg])
        final_bg=final_bg.set_duration(ttsaudio.duration)
    else:
        final_bg=stockbg
        final_bg=final_bg.set_duration(ttsaudio.duration)

    #Genetraing Composite Audio / Final Audio 
    final_audio=CompositeAudioClip([ttsaudio,final_bg])

    #Generating Stock Video 
    if (stockclip.duration < final_audio.duration):
        while (stockclip.duration < final_audio.duration):
            stockclip=concatenate_videoclips([stockclip,stockclip])
        final_video = stockclip
        final_video=final_video.set_duration(final_audio.duration)
    else:
        final_video=stockclip
        final_video=final_video.set_duration(final_audio.duration)

    final_video=final_video.set_audio(final_audio)


    # Adjusting the path
    if not (Path.endswith("/") or Path.endswith("\\") ): 
        Path = Path + "/"

    FinalPath=Path + "BeAnonymous_video.mp4"

    # Writing data into Final Video
    if add_intro == "True":
        print("ADDING INTRO")
        final_video=concatenate_videoclips([anon_intro,final_video])
        final_video.write_videofile(FinalPath)
    else:
        print("INTRO NOT ADDED")
        final_video.write_videofile(FinalPath)

# PLease Note : Subtitles are Not Yet Working!
# ~ END of function ~
        


class GenerateVideo():
    def __init__(self,video,bg,path,booleanintro,script):
        self.SampleVideo=video
        self.AudioBackground=bg
        self.OutputPath=path
        self.Include_Intro=booleanintro
        self.script=script
        generate_video(self.SampleVideo,self.AudioBackground,self.OutputPath,self.Include_Intro,self.script)
