"""Main GUI application for BeAnonymous."""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from customtkinter import StringVar, DoubleVar
from pathlib import Path
import os
import webbrowser
from PIL import Image

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
from ..core.video.generator import VideoGenerator
from ..core.utils.file_handler import FileHandler
from ..core.utils.validators import Validators

class ProgressDialog:
    """Dialog to show progress during video generation."""
    
    def __init__(self, parent):
        """Initialize progress dialog.
        
        Args:
            parent: Parent window
        """
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Generating Video")
        self.window.geometry("300x150")
        self.window.iconbitmap(str(GUI_ASSETS_PATH / APP_ICON))
        # Make it modal
        self.window.transient(parent)
        self.window.grab_set()

        
        # Center on parent
        x = parent.winfo_x() + parent.winfo_width()//2 - 150
        y = parent.winfo_y() + parent.winfo_height()//2 - 75
        self.window.geometry(f"+{x}+{y}")
        
        # Progress label
        self.label = ctk.CTkLabel(
            self.window, 
            text="Generating video...", 
            font=("Arial", 14)
        )
        self.label.pack(pady=20)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(
            self.window,
            width=250,
            height=20,
            fg_color="#2B2B2B",
            progress_color="#4a90d9"
        )
        self.progress.pack(pady=10)
        self.progress.set(0)
        
        # Status label
        self.status = ctk.CTkLabel(
            self.window,
            text="Initializing...",
            font=("Arial", 12)
        )
        self.status.pack(pady=10)
    
    def update_progress(self, value, status_text=None):
        """Update progress bar and status text.
        
        Args:
            value (float): Progress value between 0 and 1
            status_text (str, optional): Status text to display
        """
        self.progress.set(value)
        self.window.iconbitmap(str(GUI_ASSETS_PATH / APP_ICON))
        if status_text:
            self.status.configure(text=status_text)
        self.window.update()
    
    def close(self):
        """Close the dialog."""
        self.window.grab_release()
        self.window.destroy()

class BeAnonymousApp:
    """Main application class for BeAnonymous."""
    
    def __init__(self):
        """Initialize the BeAnonymous application."""
        self.window = ctk.CTk()
        self.setup_window()
        self.create_variables()
        self.load_assets()
        self.create_widgets()
        
    def setup_window(self):
        """Configure the main window."""
        self.window.title(APP_NAME)
        self.window.resizable(False, False)
        self.window.geometry(WINDOW_SIZE)
        self.window.configure(fg_color=WINDOW_BG_COLOR)
        
        # Convert relative path to absolute path for the icon
        icon_path = GUI_ASSETS_PATH / APP_ICON
        if icon_path.exists():
            self.window.iconbitmap(str(icon_path))
        
    def create_variables(self):
        """Initialize tkinter variables."""
        self.intro_var = StringVar(value="False")
        self.progress_var = DoubleVar(value=0.0)
        self.file_handler = FileHandler()
        
        # Load saved settings
        settings = FileHandler.load_settings()
        self.last_output_path = settings.get('last_output_path', '')
        
    def load_assets(self):
        """Load GUI assets."""
        self.images = {}
        for key, filename in GUI_ASSETS.items():
            file_path = GUI_ASSETS_PATH / filename
            try:
                if not file_path.exists():
                    print(f"Warning: Asset file not found: {file_path}")
                    continue
                    
                pil_image = Image.open(file_path)
                width, height = pil_image.size
                self.images[key] = ctk.CTkImage(
                    light_image=pil_image,  # Light mode image
                    dark_image=pil_image,  # Use same image for dark mode
                    size=(width, height)
                )
            except Exception as e:
                print(f"Failed to load image {filename}: {str(e)}")
                # Create an empty image as fallback
                if key in ["TOGGLE_ON", "TOGGLE_OFF"]:
                    self.images[key] = ctk.CTkImage(
                        light_image=Image.new('RGB', (62, 28), color='grey'),
                        dark_image=Image.new('RGB', (62, 28), color='grey'),
                        size=(62, 28)
                    )
                elif key in ["ABOUT_BTN", "SETTINGS_BTN"]:
                    self.images[key] = ctk.CTkImage(
                        light_image=Image.new('RGB', (30, 30), color='grey'),
                        dark_image=Image.new('RGB', (30, 30), color='grey'),
                        size=(30, 30)
                    )
                elif key == "GENERATE_BTN":
                    self.images[key] = ctk.CTkImage(
                        light_image=Image.new('RGB', (150, 40), color='grey'),
                        dark_image=Image.new('RGB', (150, 40), color='grey'),
                        size=(150, 40)
                    )
    
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
        ctk.CTkButton(
            master=self.window,
            image=self.images["ABOUT_BTN"],
            text="",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=WINDOW_BG_COLOR,
            border_width=0,
            cursor="heart",
            command=lambda: self._handle_button("about")
        ).place(x=10, y=21)
        
        # App title
        ctk.CTkLabel(
            master=self.window,
            image=self.images["APP_TITLE"],
            text="",
            fg_color="transparent"
        ).place(relx=0.5, y=37, anchor="center")
        
        # Settings button
        ctk.CTkButton(
            master=self.window,
            image=self.images["SETTINGS_BTN"],
            text="",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=WINDOW_BG_COLOR,
            border_width=0,
            cursor="pirate",
            command=lambda: self._handle_button("settings")
        ).place(x=400, y=21)
        
    def _create_output_section(self):
        """Create output directory selection section."""
        # Output Directory Label
        ctk.CTkLabel(
            master=self.window,
            text="Output Directory",
            font=("Arial", 14),
            text_color="#FFFFFF"
        ).place(x=20, y=95)

        # Decorative background image
        ctk.CTkLabel(
            master=self.window,
            image=self.images["OUTPUT_SECTION"],
            text="",
            fg_color="transparent"
        ).place(relx=0.5, y=142.5, anchor="center")

        # Entry for output path
        self.output_entry = ctk.CTkEntry(
            master=self.window,
            fg_color="#2d2d2d",
            bg_color="#2d2d2d",
            border_width=0,
            text_color="white",
            placeholder_text="Select Output Directory",
            width=350,
            height=23
        )
        self.output_entry.place(x=20, y=132)
        
        if self.last_output_path:
            self.output_entry.insert(0, self.last_output_path)
        
        # Browse button
        ctk.CTkButton(
            master=self.window,
            image=self.images["BROWSE_BTN"],
            text="",
            command=self._select_output_path,
            width=30,
            height=30,
            border_width=0,
            fg_color="#2d2d2d",
            bg_color="#2d2d2d",
            hover_color="#2d2d2d",
            cursor="hand2",
        ).place(x=385, y=128)
        
    def _create_video_section(self):
        """Create video and audio selection section."""
        # Background Video Label
        ctk.CTkLabel(
            master=self.window,
            text="Background Video",
            font=("Arial", 14),
            text_color="#FFFFFF"
        ).place(x=20, y=220)
        
        videos = self.file_handler.get_video_files()
        self.bg_video = ctk.CTkComboBox(
            master=self.window,
            values=videos,
            state="readonly",
            width=170,
            height=35,
            fg_color="#2B2B2B",
            text_color="#FFFFFF",
            button_color="#2B2B2B",
            dropdown_fg_color="#2B2B2B",
            dropdown_text_color="#FFFFFF",
            dropdown_hover_color="#404040",
            border_width=0,
            border_color="#2B2B2B"

        )
        self.bg_video.set(videos[0] if videos else "Default")
        self.bg_video.place(x=20, y=250)
        
        # Background Music Label
        ctk.CTkLabel(
            master=self.window,
            text="Background Music",
            font=("Arial", 14),
            text_color="#FFFFFF"
        ).place(x=235, y=220)
        
        audios = self.file_handler.get_audio_files()
        self.bg_music = ctk.CTkComboBox(
            master=self.window,
            values=audios,
            state="readonly",
            width=170,
            height=35,
            fg_color="#2B2B2B",
            text_color="#FFFFFF",
            button_color="#2B2B2B",
            dropdown_fg_color="#2B2B2B",
            dropdown_text_color="#FFFFFF",
            dropdown_hover_color="#404040",
            border_color="#2B2B2B",
            border_width=0
        )
        self.bg_music.set(audios[0] if audios else "Default")
        self.bg_music.place(x=235, y=250)
        
        # Anonymous Intro Label
        ctk.CTkLabel(
            master=self.window,
            text="Include Anonymous Intro?",
            font=("Arial", 14),
            text_color="#FFFFFF"
        ).place(x=80, y=170)
        
        self.toggle_btn = ctk.CTkButton(
            master=self.window,
            image=self.images["TOGGLE_OFF"],
            text="",
            width=62,
            height=28,
            border_width=0,
            fg_color="transparent",
            hover_color=WINDOW_BG_COLOR,
            command=self._toggle_intro
        )
        self.toggle_btn.place(x=10, y=170)
        
    def _create_script_section(self):
        """Create script input section."""
        # Enter Script Label
        ctk.CTkLabel(
            master=self.window,
            text="Enter Script of Video",
            font=("Arial", 14),
            text_color="#FFFFFF"
        ).place(x=20, y=305)

        ctk.CTkLabel(
            master=self.window,
            text="",
            image=self.images["SCRIPT_ENTRY_BACKGROUND"],
            fg_color="transparent"
        ).place(relx=0.5, y=400, anchor="center")
        
        self.script_entry = ctk.CTkTextbox(
            master=self.window,
            fg_color="#2d2d2d",
            bg_color="#2d2d2d",
            text_color="white",
            font=("Arial", 16),
            border_width=0,
            width=403,
            height=115,
        )
        self.script_entry.place(x=22, y=342)
        
    def _create_generate_button(self):
        """Create generate button."""
        self.generate_btn = ctk.CTkButton(
            master=self.window,
            image=self.images["GENERATE_BTN"],
            text="",
            width=150,
            height=40,
            border_width=0,
            fg_color="transparent",
            hover_color=WINDOW_BG_COLOR,
            command=lambda: self._handle_button("generate")
        )
        self.generate_btn.place(x=10, y=475)
        
    def _handle_button(self, action):
        """Handle button clicks."""
        if action == "about":
            webbrowser.open(GITHUB_URL)
        elif action == "settings":
            messagebox.showinfo("Settings", "Version: 1.0.0\nWords per Minute: 200")
        elif action == "generate":
            self._generate_video()
            
    def _select_output_path(self):
        """Handle output directory selection."""
        path = filedialog.askdirectory()
        if path:
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, path)
            FileHandler.save_settings({'last_output_path': path})
            
    def _toggle_intro(self):
        """Toggle intro video inclusion."""
        current_state = self.intro_var.get()
        new_state = "False" if current_state == "True" else "True"
        toggle_state = 'ON' if new_state == "True" else 'OFF'
        self.toggle_btn.configure(
            image=self.images[f"TOGGLE_{toggle_state}"]
        )
        self.intro_var.set(new_state)
            
    def _validate_selections(self):
        """Validate all user selections before generation."""
        if not self.script_entry.get("1.0", "end").strip():
            raise ValueError(ERROR_MSGS["EMPTY_FIELDS"])
            
        if not self.file_handler.validate_output_path(self.output_entry.get()):
            raise ValueError(ERROR_MSGS["INVALID_PATH"])
            
        if self.bg_video.get() == "Default" or self.bg_music.get() == "Default":
            raise ValueError("Please select background video and music")

    def _generate_video(self):
        """Handle video generation process."""
        try:
            self.generate_btn.configure(state="disabled")
            
            # Validate all inputs first
            self._validate_selections()
            
            # Create and show progress dialog
            progress_dialog = ProgressDialog(self.window)
            
            # Generate TTS
            progress_dialog.update_progress(0.1, "Generating Text-to-Speech...")
            tts = TTS(self.script_entry.get("1.0", "end").strip())
            if not tts.generate():
                raise Exception("TTS generation failed")
            
            progress_dialog.update_progress(0.4, "Text-to-Speech generated...")
            
            # Generate video with progress updates
            generator = VideoGenerator(
                self.bg_video.get(),
                self.bg_music.get(),
                self.output_entry.get(),
                self.intro_var.get() == "True"
            )
            
            def progress_callback(value):
                # Convert 0-100 to 0.4-1.0 range for overall progress
                progress = 0.4 + (value * 0.6 / 100)
                status = "Processing video..." if value < 100 else "Finalizing..."
                progress_dialog.update_progress(progress, status)
            
            if not generator.generate(progress_callback=progress_callback):
                raise Exception("Video generation failed")
            
            # Close progress dialog
            progress_dialog.close()
            
            result = messagebox.askquestion(
                "Success", 
                SUCCESS_MSG.format(self.output_entry.get()) + "\n\nWould you like to open the video?", 
                type='yesno'
            )
            if result == 'yes':
                self._open_generated_video()
            
        except Exception as e:
            try:
                progress_dialog.close()
            except:
                pass
            messagebox.showerror("Error", str(e))
        finally:
            self.generate_btn.configure(state="normal")
            
    def _open_generated_video(self):
        """Open the generated video file."""
        from ..config.settings import VIDEO_OUTPUT_FILENAME
        try:
            video_path = Path(self.output_entry.get()) / VIDEO_OUTPUT_FILENAME
            if video_path.exists():
                os.startfile(str(video_path))
            else:
                messagebox.showerror("Error", f"Video file not found at {video_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open video: {str(e)}")
            
    def run(self):
        """Start the application."""
        self.window.mainloop()