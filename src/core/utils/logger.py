"""Centralized logging configuration for BeAnonymous."""
import logging
import sys

class CustomFormatter(logging.Formatter):
    """Custom formatter with component prefixes."""
    
    def format(self, record):
        # Add brackets to the component name if not already present
        if not record.name.startswith('[') and not record.name.endswith(']'):
            record.name = f'[{record.name}]'
        return super().format(record)

def setup_logger():
    """Setup and configure the central logger."""
    # Create logger
    logger = logging.getLogger('beanonymous')
    logger.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = CustomFormatter('%(name)s %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

# Create the central logger instance
logger = setup_logger()

def get_logger(component_name: str) -> logging.Logger:
    """Get a logger for a specific component.
    
    Args:
        component_name (str): Name of the component (e.g., 'TTS', 'GENERATOR')
        
    Returns:
        logging.Logger: Logger instance for the component
    """
    return logging.getLogger(f'beanonymous.{component_name}')
