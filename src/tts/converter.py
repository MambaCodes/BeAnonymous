import subprocess



# FILE PATHS : 
inputfile="src/temp/normal_audio.mp3" # Path for the Original TTS
outputfile="src/temp/final_tts.mp3" # Path for the Final tts output
ffmpeg="src/ffmpeg/ffmpeg.exe"


def delete_original_tts():
    try:
        import os
        os.remove(inputfile)
        print("\n[CONVERTER] Success : Original TTS has been deleted")
    except Exception as error:
        print("\n[CONVERTER] Failure : Original TTS has not been deleted")
        print(error)


def precheck_outputfile():
    import os
    if os.path.exists(outputfile):
        os.remove(outputfile)
        print("\n\n[CONVERTER] Success : Outputfile has been deleted")



'''
FFMPEG command : 
For Low Pitch  : ffmpeg -i {inputfile} -af asetrate=44100*0.35,aresample=44100 {outputfile}
For High Pitch : ffmpeg -i {inputfile} -af asetrate=44100*1.15,aresample=44100 {outputfile}
'''


def lower_pitch():
    precheck_outputfile()
    try:
        subprocess.call([ffmpeg, "-i", inputfile, "-af", "asetrate=44100*0.35,aresample=44100", outputfile])
        print("\n\n[CONVERTER] Success : Pitch has been changed to - LOW ")
        delete_original_tts()
    except Exception as error:
        print("\n\n[CONVERTER] Failure : Pitch has not been changed to - LOW ")
        print(error)
            
def higher_pitch():
    # but for converting in high pitch, we  will also need to 
    # Decrease the rate of speech of the original Generated TTS in the tts_generator.py
    # Because increasing pitch would also increase the Rate of Speech/Words per Minute.
    precheck_outputfile()
    try:
        subprocess.call([ffmpeg, "-i", inputfile, "-af", "asetrate=44100*1.5", outputfile])
        print("\n\n[CONVERTER] Success : Pitch has been changed to - HIGH ")
        delete_original_tts()
    except Exception as error:
        print("\n\n[CONVERTER] Failure : Pitch has not been changed to - HIGH ")
        print(error)





class Converter():
    option="pitchtolow" # Default it is SET to lower the Pitch
    # Change ".option" in instance if user wants to change into High Pitch
        
    def convert_pitch(self):
        try:
            if self.option=="pitchtohigh":
                higher_pitch()
            elif self.option=="pitchtolow":
                lower_pitch()
            else:
                print("\n\nInvalid Pitch Option {self.option}\nAvaliable Calls for Pitch Function :\n1.tohigh\ntolow\n")
                return
        except Exception as error:
            print("\n\n[CONVERTER] Failure : Convert Pitch Function was not Executed")
            print(error)

