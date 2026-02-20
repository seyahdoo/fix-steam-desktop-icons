import os
import winreg
import logging
import re

class WindowsSteamFinder:
    """Implementation for locating Steam installation directory on Windows."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def find_steam_install_path(self) -> str:
        """Find the Steam installation path."""
        # 1. Try default location
        default_path = r"C:\Program Files (x86)\Steam"
        self._logger.debug(f"Checking default location: {default_path}")
        if os.path.exists(os.path.join(default_path, "steam.exe")):
            self._logger.info(f"Found Steam installation at default location: {default_path}")
            return default_path
        
        # 2. Try reading from Windows registry
        self._logger.debug("Attempting to find Steam path through Registry...")
        try:
            with winreg.ConnectRegistry(None, winreg.HKEY_CLASSES_ROOT) as access_registry:
                with winreg.OpenKey(access_registry, r"steam\Shell\Open\Command") as access_key:
                    reg_value, _ = winreg.EnumValue(access_key, 0)
            
            self._logger.debug(f"Registry raw value: {reg_value}")
            
            # Robustly parse path using regex to handle quoted or unquoted paths with arguments
            # Matches anything ending in steam.exe, capturing the full path
            match = re.search(r'("?)(.+?steam\.exe)\1', reg_value, re.IGNORECASE)
            
            if match:
                steam_exe_path = match.group(2)
                steam_install_folder = os.path.dirname(steam_exe_path)
                
                if os.path.exists(steam_install_folder):
                    self._logger.info(f"Successfully located Steam via Registry: {steam_install_folder}")
                    return steam_install_folder
                else:
                    self._logger.error(f"Path from Registry does not exist: {steam_install_folder}")
            else:
                self._logger.error(f"Could not parse steam.exe path from registry value: {reg_value}")

        except Exception as e:
            self._logger.error(f"Failed to read Registry: {str(e)}")
            
        raise Exception("Steam installation folder not found! Please ensure Steam is installed.")
