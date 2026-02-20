import os
import json
import logging
from typing import List

class DesktopConfigLoader:
    """Helper class for loading desktop path configuration."""

    def __init__(self, config_file: str = "custom_location.json"):
        self._config_file = config_file
        self._logger = logging.getLogger(__name__)

    def get_desktop_paths(self) -> List[str]:
        """Get desktop paths to scan.
        
        Priority:
        1. If config file exists and contains valid directory, use ONLY that custom path.
        2. If no valid custom path, fallback to system default desktop locations.
        """
        # 1. Try to load custom path from config
        if os.path.exists(self._config_file):
            try:
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    custom_path = config.get("desktop_path")
                    if custom_path and os.path.isdir(custom_path):
                        self._logger.info(f"Using custom desktop path: {custom_path}")
                        return [custom_path]
            except Exception as e:
                self._logger.warning(f"Failed to read config file, falling back to defaults: {str(e)}")

        # 2. Fallback to system default paths
        self._logger.debug("No valid custom path found. Retrieving system default desktop locations.")
        attempted_paths = []
        user_profile = os.environ.get("USERPROFILE")
        if user_profile:
            attempted_paths.append(os.path.join(user_profile, 'Desktop'))
            attempted_paths.append(os.path.join(user_profile, 'OneDrive', 'Desktop'))
        
        self._logger.debug(f"Attempting to check system default paths: {attempted_paths}")
        
        valid_defaults = [p for p in attempted_paths if os.path.isdir(p)]
        
        if valid_defaults:
            self._logger.info(f"Identified valid system desktop paths: {valid_defaults}")
        else:
            self._logger.warning(f"None of the attempted system paths exist: {attempted_paths}")
            
        return valid_defaults
