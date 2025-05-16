"""Settings management utilities for BeAnonymous."""
import json
from pathlib import Path
from ..utils.logger import get_logger

logger = get_logger('SETTINGS')

class SettingsManager:
    """Centralized settings management for the application."""
    SETTINGS_FILE = Path.home() / ".beanonymous" / "settings.json"
    
    # Default settings
    DEFAULT_SETTINGS = {
        'tts_rate': 195,
        'tts_voice_id': 0,
        'pitch_factor': 0.35,
        'last_output_path': ''
    }
    
    
    @classmethod
    def load_settings(cls):
        """Load settings from file."""
        try:
            if cls.SETTINGS_FILE.exists():
                with open(cls.SETTINGS_FILE, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**cls.DEFAULT_SETTINGS, **settings}
            else:
                logger.info("No settings file found, using defaults")
                return dict(cls.DEFAULT_SETTINGS)
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            return dict(cls.DEFAULT_SETTINGS)
    
    @classmethod
    def save_settings(cls, settings):
        """Save settings to file.
        
        Args:
            settings (dict): Settings to save
        """
        try:
            # Create settings directory if it doesn't exist
            cls.SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            # Merge with current settings to preserve other values
            current_settings = cls.load_settings()
            current_settings.update(settings)
            
            with open(cls.SETTINGS_FILE, 'w') as f:
                json.dump(current_settings, f)
                
            logger.info("Settings saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    @classmethod
    def get_setting(cls, key, default=None):
        """Get a single setting value.
        
        Args:
            key (str): Setting key to get
            default: Default value if setting doesn't exist
            
        Returns:
            Setting value or default
        """
        settings = cls.load_settings()
        return settings.get(key, default)
