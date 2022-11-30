import pyttsx3

engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
engine.setProperty('rate',200)

def generate_normal_tts(audio,path):
    #engine.save_to_file("<pitch absmiddle='-10' middle='-10'>" + audio + "</pitch>" ,path)
    engine.save_to_file(audio,path)
    engine.runAndWait()


class TTS():
    def __init__(self,entered_text):
        self.text = entered_text

    path="src/temp/"
    name_of_file="normal_audio.mp3"

    def generate(self):
        try:
            generate_normal_tts(self.text,self.path+self.name_of_file)
            print(" [TTS GENERATOR] Success : Normal TTS has been Generated")
        except Exception as error:
            print(" [TTS GENERATOR] Failure : Normal TTS has not been Generated")
            print(error)
            
    @classmethod
    def change_path(cls,newpath):
        cls.path=newpath

    @classmethod
    def change_name(self,newname):
        self.name_of_file=newname
    
    

        
       

#For Testing How this Works :

# Firstly input text to generate into speech
#text_by_user = input(">")

# Declaring TTS Instance :
#output=TTS(text_by_user)

# Changing path of output file
#output.change_path("src/")

# Changing name of output file
#output.change_name("newname.mp3")

# Generating TTS
#output.generate()



