"""Main GUI application for BeAnonymous."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import os
import webbrowser

from ..config.settings import (
    APP_NAME, 
    WINDOW_SIZE, 
    WINDOW_BG_COLOR,
    GUI_ASSETS_PATH,
    TEMP_PATH
)
from ..config.constants import (
    GUI_ASSETS,
    APP_ICON,
    SUCCESS_MSG,
    ERROR_MSGS,
    GITHUB_URL
)
from ..core.audio.tts import TTS
from ..core.audio.processor import AudioProcessor
from ..core.video.generator import VideoGenerator
from ..core.utils.file_handler import FileHandler
from ..core.utils.validators import Validators

class BeAnonymousApp:
    """Main application class for BeAnonymous."""
    
    def __init__(self):
        """Initialize the BeAnonymous application."""
        self.window = tk.Tk()
        self.setup_window()
        self.create_variables()
        self.load_assets()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window."""
        self.window.title(APP_NAME)
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(bg=WINDOW_BG_COLOR)
        
        # Convert relative path to absolute path for the icon
         # Use pathlib for path handling
        icon_path = GUI_ASSETS_PATH / APP_ICON
        if icon_path.exists():
            self.window.iconbitmap(str(icon_path))
        
        self.canvas = tk.Canvas(
            self.window,
            bg=WINDOW_BG_COLOR,
            height=600,
            width=450,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        
    def create_variables(self):
        """Initialize tkinter variables."""
        self.intro_var = tk.StringVar(value="False")
        self.file_handler = FileHandler()
        
    def load_assets(self):
        """Load GUI assets."""
        self.images = {}
        for key, filename in GUI_ASSETS.items():
            file_path = GUI_ASSETS_PATH / filename
            try:
                self.images[key] = tk.PhotoImage(file=str(file_path))
            except tk.TclError as e:
                print(f"Failed to load image {filename}: {e}")
    
    def create_widgets(self):
        """Create and place all GUI widgets."""
        self._create_header()
        self._create_output_section()
        self._create_video_section()
        self._create_script_section()
        self._create_generate_button()
        
    def _create_header(self):
        """Create header section with logo and buttons."""
        # About button
        tk.Button(
            image=self.images["ABOUT_BTN"],
            borderwidth=0,
            highlightthickness=0,
            activebackground=WINDOW_BG_COLOR,
            cursor="heart",
            command=lambda: self._handle_button("about"),
            relief="flat"
        ).place(x=20, y=21, width=30, height=30)
        
        # App title
        self.canvas.create_image(225, 37, image=self.images["APP_TITLE"])
        
        # Settings button
        tk.Button(
            image=self.images["SETTINGS_BTN"],
            borderwidth=0,
            highlightthickness=0,
            activebackground=WINDOW_BG_COLOR,
            cursor="pirate",
            command=lambda: self._handle_button("settings"),
            relief="flat"
        ).place(x=400, y=21, width=30, height=30)
        
    def _create_output_section(self):
        """Create output directory selection section."""
        self.canvas.create_image(224.5, 137.5, image=self.images["OUTPUT_SECTION"])
        
        self.output_entry = tk.Entry(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.output_entry.place(x=50, y=127, width=350, height=23)
        
        tk.Button(
            text="Browse",
            command=self._select_output_path
        ).place(x=190, y=160, width=70, height=25)
        
    def _create_video_section(self):
        """Create video and audio selection section."""
        # Video selector
        self.bg_video = ttk.Combobox(
            values=self.file_handler.get_video_files(),
            state="readonly"
        )
        self.bg_video.set("Default")
        self.bg_video.place(x=50, y=220, width=350, height=25)
        
        # Audio selector
        self.bg_music = ttk.Combobox(
            values=self.file_handler.get_audio_files(),
            state="readonly"
        )
        self.bg_music.set("Default")
        self.bg_music.place(x=50, y=270, width=350, height=25)
        
        # Intro toggle
        self.toggle_btn = tk.Button(
            image=self.images["TOGGLE_OFF"],
            borderwidth=0,
            highlightthickness=0,
            command=self._toggle_intro,
            relief="flat"
        )
        self.toggle_btn.place(x=50, y=320, width=62, height=28)
        
    def _create_script_section(self):
        """Create script input section."""
        self.script_entry = tk.Text(
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        self.script_entry.place(x=50, y=370, width=350, height=150)
        
    def _create_generate_button(self):
        """Create generate button."""
        self.generate_btn = tk.Button(
            image=self.images["GENERATE_BTN"],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self._handle_button("generate"),
            relief="flat"
        )
        self.generate_btn.place(x=150, y=540, width=150, height=40)
        
    def _handle_button(self, action):
        """Handle button clicks.
        
        Args:
            action (str): Button action to handle
        """
        if action == "about":
            webbrowser.open(GITHUB_URL)
        elif action == "settings":
            messagebox.showinfo("Settings", "Version: 1.0.0\nWords per Minute: 200")
        elif action == "generate":
            self._generate_video()
            
    def _select_output_path(self):
        """Handle output directory selection."""
        path = filedialog.askdirectory()
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, path)
        
    def _toggle_intro(self):
        """Toggle intro video inclusion."""
        if self.intro_var.get() == "True":
            self.toggle_btn.configure(image=self.images["TOGGLE_OFF"])
            self.intro_var.set("False")
        else:
            self.toggle_btn.configure(image=self.images["TOGGLE_ON"])
            self.intro_var.set("True")
            
    def _generate_video(self):
        """Handle video generation process."""
        try:
            
            # Debugging output [TODO: REMOVE before merging]
            print(f"TEMP_PATH: {TEMP_PATH}")
            print(f"TEMP_PATH exists: {TEMP_PATH.exists()}")
        

            # Disable generate button
            self.generate_btn.configure(state="disabled")
            
            # Validate inputs
            if not Validators.validate_script(self.script_entry.get("1.0", tk.END)):
                raise ValueError(ERROR_MSGS["EMPTY_FIELDS"])
                
            if not self.file_handler.validate_output_path(self.output_entry.get()):
                raise ValueError(ERROR_MSGS["INVALID_PATH"])
            
            # Generate TTS audio with pitch adjustment
            tts = TTS(self.script_entry.get("1.0", tk.END))
            if not tts.generate():
                raise Exception("TTS generation failed")
                
            # Generate video
            generator = VideoGenerator(
                self.bg_video.get(),
                self.bg_music.get(),
                self.output_entry.get(),
                self.intro_var.get() == "True"
            )
            if not generator.generate():
                raise Exception("Video generation failed")
                
            messagebox.showinfo("Success", SUCCESS_MSG.format(self.output_entry.get()))
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.generate_btn.configure(state="normal")
            
    def run(self):
        """Start the application."""
        self.window.mainloop()
