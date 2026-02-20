import os
import winreg
import logging
from typing import List

class DesktopConfigLoader:
    """Helper class for loading desktop path configuration."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_desktop_paths(self) -> List[str]:
        """Get desktop paths to scan.
        
        Logic:
        1. Query Windows Registry for the current user's Desktop folder.
        2. Include standard default locations as fallbacks.
        3. Return a list of unique, existing directories.
        """
        desktop_directories = set()
        
        # 1. Query Registry
        try:
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                desktop_path_reg, _ = winreg.QueryValueEx(key, "Desktop")
                # Expand environment variables (e.g., %USERPROFILE%)
                expanded_path = os.path.expandvars(desktop_path_reg)
                if os.path.isdir(expanded_path):
                    self._logger.info(f"Found Registry Desktop path: {expanded_path}")
                    desktop_directories.add(expanded_path)
        except Exception as e:
            self._logger.warning(f"Failed to query Registry for Desktop path: {str(e)}")

        # 2. Add Standard Defaults
        user_profile = os.environ.get("USERPROFILE")
        if user_profile:
            possible_defaults = [
                os.path.join(user_profile, 'Desktop'),
                os.path.join(user_profile, 'OneDrive', 'Desktop')
            ]
            for path in possible_defaults:
                if os.path.isdir(path):
                    desktop_directories.add(path)
        
        valid_paths = list(desktop_directories)
        
        if valid_paths:
            self._logger.info(f"Identified valid desktop paths to scan: {valid_paths}")
        else:
            self._logger.error("No valid desktop paths could be found.")
            
        return valid_paths
