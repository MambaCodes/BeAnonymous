"""Settings configuration for BeAnonymous."""

from pathlib import Path

# Base Directory Structure
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = ROOT_DIR / 'src'

# Application Directory Structure
CORE_DIR = SRC_DIR / 'core'
CONFIG_DIR = SRC_DIR / 'config'
GUI_DIR = SRC_DIR / 'gui'
RESOURCES_DIR = SRC_DIR / 'resources'

# Feature-specific Paths
GUI_ASSETS_PATH = GUI_DIR / 'assets'
VIDEO_ASSETS_PATH = RESOURCES_DIR / 'videos'
AUDIO_ASSETS_PATH = RESOURCES_DIR / 'audio'
TEMP_PATH = CORE_DIR / 'utils' / 'temp'

# Media Paths
INTRO_VIDEO_PATH = VIDEO_ASSETS_PATH / 'intro' / 'anon_intro.mp4'

# Ensure critical directories exist
REQUIRED_DIRS = [
    TEMP_PATH,
    GUI_ASSETS_PATH,
    VIDEO_ASSETS_PATH,
    AUDIO_ASSETS_PATH
]

# Create directories if they don't exist
for directory in REQUIRED_DIRS:
    directory.mkdir(parents=True, exist_ok=True)

# Application Settings
APP_NAME = "BeAnonymous"
APP_VERSION = "1.0.0"
WINDOW_SIZE = "450x600"
WINDOW_BG_COLOR = "#202020"

# Video Settings
DEFAULT_VIDEO = "Default"
DEFAULT_AUDIO = "Default"
VIDEO_OUTPUT_FILENAME = "BeAnonymous_video.mp4"

# TTS Settings
TTS_RATE = 200
TTS_VOICE_ID = 0
TTS_TEMP_FILE = TEMP_PATH / 'normal_audio.mp3'
TTS_FINAL_FILE = TEMP_PATH / 'final_tts.mp3'