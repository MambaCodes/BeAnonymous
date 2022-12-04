

# Importing BACKEND FUNCTIONS & CLASSES
from tts.tts_generator import TTS
from tts.converter import Converter
from video.video_generator import GenerateVideo


# Importing GUI Libraries : 
from pathlib import Path
import webbrowser
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage,filedialog,END,ttk,Variable,messagebox



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("gui/assets/")



def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# Main Function That Generates the Video
def GENERATE():
    # Showing Values from GUI
    print("Generate Button Clicked")
    print("Path: ",output_entry.get())
    print("Include Intro: ",onoff.get())
    print("Video: ",bg_video.current())
    print("Music: ",bg_music.current())
    print("Script: ",script_entry.get("1.0",END))

    #           Backend 
    # TTS audio generation
    engine=TTS(script_entry.get("1.0",END))
    engine.generate() # Generates Normal TTS
    converter=Converter()
    converter.convert_pitch()
    # TTS audio generation output --> final_tts.mp3

    # VIDEO generation
    GenerateVideo(bg_video.get(),bg_music.get(),output_entry.get(),onoff.get(),script_entry.get("1.0",END))
    # VIDEO generation output --> BeAnonymous_video.mp4

    # shoiwing a message for Successful Video Generation
    messagebox.showinfo("Success","Video Generated Successfully at "+ output_entry.get())


# Functions for ComboBox (Stock Video & Audio Selectors)
def get_list_of_bg_videos():
    import os
    video_list=[]
    for i in os.listdir("src/video/assets/"):
        if i.endswith(".mp4"):
            video_list.append(str(i).replace(".mp4",""))
    return video_list
def get_list_of_bg_music():
    import os
    music_list=[]
    for i in os.listdir("src/video/assets/"):
        if i.endswith(".mp3"):
            music_list.append(str(i).replace(".mp3",""))
    return music_list


# Function for Selecting Output Directory
def select_output_path():
    entered_path = filedialog.askdirectory()
    output_entry.delete(0, END)
    output_entry.insert(0, entered_path)


# Function for Controling button Presses
def handle_btn_press(option):
    if option=="about":
        print("About Button Clicked")
        webbrowser.open("https://github.com/mambacodes/beanonymous")
    elif option=="settings":
        print("settings Button Clicked")
        messagebox.showinfo("Settings","Version : 1.0.0\nWords per Minute : 200")
    elif option=="generate":
        try : 
            GENERATE()
        except Exception as e:
            messagebox.showerror("Error",e)


# Functions for Toggle Button
def toggle_on():
    toggle_img.configure(file=relative_to_assets("togglebtn_on.png"))
    toggle_btn.configure(command=toggle_off)
    onoff.set(value="True")
def toggle_off():
    toggle_img.configure(file=relative_to_assets("togglebtn_off.png"))
    toggle_btn.configure(command=toggle_on)
    onoff.set(value="False")
    


# GUI starts here : 
window = Tk()
window.title("BeAnonymous")
window.geometry("450x600")
window.configure(bg = "#202020")
window.iconbitmap(relative_to_assets("beanonymous.ico"))

canvas = Canvas(
    window,
    bg = "#202020",
    height = 600,
    width = 450,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)


# About Button
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    activebackground= "#202020",
    cursor="heart",
    command=lambda : handle_btn_press("about"),
    relief="flat"
)
button_3.place(
    x=20.0,
    y=21.0,
    width=30.0,
    height=30.0
)



# App Title
image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    225.0,
    37.0,
    image=image_image_6
)


# Settings Button
button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    activebackground= "#202020",
    cursor="pirate",
    command=lambda : handle_btn_press("settings"),
    relief="flat"
)
button_4.place(
    x=400.0,
    y=21.0,
    width=30.0,
    height=30.0
)


    
# Output Selection section
image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    224.5,
    137.5,
    image=image_image_5
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    210.0,
    138.0,
    image=entry_image_1
)

output_entry = Entry(
    bd=0,
    bg="#2D2D2D",
    fg="#FFFFFF",
    highlightthickness=0
)
output_entry.place(
    x=37.0,
    y=123.0,
    width=346.0,
    height=30.0
)

# Output Dir Button
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=select_output_path,
    activebackground= "#202020",
    cursor="target",
    relief="flat"
)
button_2.place(
    x=402.0,
    y=130.39999389648438,
    width=16.0,
    height=15.20001220703125
)

canvas.create_text(
    20.0,
    98.0,
    anchor="nw",
    text="Output directory",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)



# "Include Anonymous Intro" Toggle Button
canvas.create_text(
    75.0,
    178.0,
    anchor="nw",
    text="Include Anonymous Intro",
    fill="#FFFFFF",
    font=("Roboto Regular", 14 * -1)
)
toggle_img = PhotoImage(
    file=relative_to_assets("togglebtn_off.png"))

onoff=Variable(value="False") # For backend! 
toggle_btn=Button(
    image=toggle_img,
    activebackground= "#202020",
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=toggle_on,
)
toggle_btn.place(
    x=27.0,
    y=175.0
)



# COMBOBOXES : 

#               1. Background Video selector
canvas.create_text(
    25.0,
    235.0,
    anchor="nw",
    text="Background Video",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)
bg_video=ttk.Combobox(
    values=get_list_of_bg_videos(),
    state="readonly",
    justify="center",
    font=("Roboto Regular", 14 * -1)
)
bg_video.current(0) # For Setting the Standard Video as Default
                    # Though i know this won't work Correctly
                    # will be changed in Future Commits
bg_video.place(
    x=24.0,
    y=257.0,
    width=182.0,
    height=34.0
)

#               2. Background Music Selector
bg_music=ttk.Combobox(
    values=get_list_of_bg_music(),
    state="readonly",
    justify="center",
    font=("Roboto Regular", 14 * -1)
)
bg_music.current(0)
bg_music.place(
    x=240.0,
    y=257.0,
    width=182.0,
    height=34.0
)
canvas.create_text(
    238.0,
    235.0,
    anchor="nw",
    text="Background Music",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)



# Input Script Section
canvas.create_text(
    29.0,
    338.0,
    anchor="nw",
    text="Enter Script of Video",
    fill="#FFFFFF",
    font=("Roboto Medium", 14 * -1)
)

#       Input Script Box Background Image (#202020 image*)
scriptbox_color_image = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    226.0,
    421.0,
    image=scriptbox_color_image
)

#       Script entry Image (Particular Lined Box)
scriptbox_image = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    225.5,
    420.0,
    image=scriptbox_image
)

#       Entry Box :
script_entry = Text(
    bd=0,
    bg="#2D2D2D",
    fg="white",
    font=("Roboto Medium", 14 * -1),
    highlightthickness=0
)
script_entry.place(
    x=38.0,
    y=371.0,
    width=375.0,
    height=96.0
)


# Generate Button
generate_button_image = PhotoImage(
    file=relative_to_assets("button_1.png"))
generate_btn = Button(
    image=generate_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda : handle_btn_press("generate"),
    activebackground= "#202020",
    relief="flat"
)
generate_btn.place(
    x=18.0,
    y=532.0,
    width=414.0,
    height=47.0
)


window.resizable(False, False)
window.mainloop()

# End of GUI Code