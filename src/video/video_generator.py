from moviepy.editor import *



# REMAKE THIS SCRIPT!!


# for Generate Stock Videos
# Combining Two Videos : 
#ffmpeg -f concat -i file "C:\a\b\01.mp4" file "C:\a\b\02.mp4" -codec copy output.mp4


# For generating Durations
# Use MoviePys .duration instead.
# or
# getting Duration of an Audio File :
# ffprobe -v error -show_entries format=duration \
# -of default=noprint_wrappers=1:nokey=1 input.mp4

# For Triming Video 
# Use moviepy .SetDuration


# For Combining The Audios :
# ffmpeg -i "concat:audio1.mp3|audio2.mp3" -acodec copy output.mp3
# or
# Moviepys : CompositeAudioClip([audio, SampleAudio])


# For Combining The Videos , Audios :
# Moviepy :
# final_video= CompositeAudioClip([samplevideo,final_audio])
# here final_audio : TTS + background.



'''
def GenerateStockVideo(audiofile,videofile):
    while (videofile.duration<audiofile.duration):
        #ffmpeg -f concat -i file "C:\a\b\01.mp4" file "C:\a\b\02.mp4" -codec copy output.mp4
        try:
            subprocess.call([ffmpeg, "-f", "concat", "-i", "file", "src/video/assets/new.mp4", "file", "src/video/assets/new.mp4", "-codec", "copy", "src/temp/stockvideo.mp4"])
        except Exception as e:
            print("[VIDEO GENERATOR] Failure : Stock Video Generation Failed,\n",e)
        return "src/temp/stockvideo.mp4"
    
def GenerateBackgroundSong(audiofile,videofile):
    # This Function will Convert the length of Audio File
    if(audiofile.duration < videofile.duration):
        while (audiofile.duration<videofile.duration):
            clips=[audiofile,audiofile]
            audiofile= concatenate_audioclips(clips)
        audiofile = audiofile.set_duration(videofile.duration)
    else:
        audiofile = audiofile.set_duration(videofile.duration)

def generate_video(video,bg):
    try:
        SampleVideo = VideoFileClip("src/video/assets/" + video + ".mp4")
        SampleAudio = AudioFileClip("src/video/assets/" + bg + ".mp3")
        audio = AudioFileClip("src/temp/final_audio.mp3")
        if audio.duration >= SampleVideo.duration:
            GenerateStockVideo(audio,SampleVideo) #Generating the Sample Video
            GenerateBackgroundSong(SampleAudio,SampleVideo) #Generating the Sample Audio
            while(SampleVideo.duration<audio.duration):
                clips=[SampleVideo,SampleVideo]
                SampleVideo= concatenate_videoclips(clips)
            SampleVideo = SampleVideo.set_duration(audio.duration)

        else:
            SampleVideo = SampleVideo.set_duration(audio.duration)
            GenerateBackgroundSong(SampleAudio,SampleVideo)

            
        # Adding the TTS Audio and background Song. 
        final_audio= CompositeAudioClip([audio, SampleAudio])
        final_video=SampleVideo.set_audio(final_audio)

        # Writing To the Final Video
        final_video.write_videofile("src/temp/final_video.mp4")

                
        print("\n\n[VIDEO GENERATOR] Video Generated")

    except Exception as e:
        print("\n\n[VIDEO GENERATOR] Error Occured: ",e)
        print("\n[VIDEO GENERATOR] Video Generation Failed")
'''




def generate_video(SampleVideo,AudioBackground):
    print("Func called")
    ttsaudio=AudioFileClip("src/temp/final_tts.mp3")
    stockclip=VideoFileClip("src/video/assets/" + SampleVideo + ".mp4")
    stockbg=AudioFileClip("src/video/assets/" + AudioBackground + ".mp3")
    print("Starting dumb shit")
    #Genetraing Background Audio
    if (stockbg.duration < ttsaudio.duration):
        while (stockbg.duration < ttsaudio.duration):
            final_bg=concatenate_audioclips([stockbg,stockbg])
        final_bg=final_bg.set_duration(ttsaudio.duration)
    else:
        final_bg=stockbg
        final_bg=final_bg.set_duration(ttsaudio.duration)

    print('Andrew Tate')
    #Genetraing Composite Audio / Final Audio 
    final_audio=CompositeAudioClip([ttsaudio,final_bg])

    print("I have a deal for you")
    #Generating Stock Video 
    if (stockclip.duration < final_audio.duration):
        print("before while")
        while (stockclip.duration < final_audio.duration):
            stockclip=concatenate_videoclips([stockclip,stockclip])
            print("doing while")
        final_video = stockclip
        final_video=final_video.set_duration(final_audio.duration)
        print("while done")
    else:
        final_video=stockclip
        final_video=final_video.set_duration(final_audio.duration)

    final_video=final_video.set_audio(final_audio)


    # Writing data into Final Video
    final_video.write_videofile("src/temp/output_video.mp4")

# ~ END of function ~
        


class GenerateVideo():
    def __init__(self,video,bg):
        self.SampleVideo=video
        self.AudioBackground=bg
        generate_video(self.SampleVideo,self.AudioBackground)

#GenerateVideo("new","aud_1")
