import os
import logging
from typing import List, Optional
from src.models import SteamShortcut

class FileSystemShortcutProvider:
    """Implementation for reading and parsing Steam shortcuts from the file system."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def get_shortcuts(self, search_paths: List[str]) -> List[SteamShortcut]:
        """Scan multiple paths for Steam shortcuts."""
        shortcuts = []
        for path in search_paths:
            if not os.path.isdir(path):
                self._logger.debug(f"Skipping invalid path: {path}")
                continue
            
            self._logger.debug(f"Scanning directory: {path}")
            try:
                for filename in os.listdir(path):
                    if filename.endswith(".url"):
                        file_path = os.path.join(path, filename)
                        shortcut = self._parse_url_file(file_path)
                        if shortcut:
                            shortcuts.append(shortcut)
                        # Output a blank line to group logs for this shortcut
                        print("")
            except Exception as e:
                self._logger.error(f"Error scanning directory {path}: {str(e)}")
        
        return shortcuts

    def _parse_url_file(self, file_path: str) -> Optional[SteamShortcut]:
        """Parse a single .url file."""
        try:
            self._logger.debug(f"Parsing shortcut: {file_path}")
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.readlines()
            
            game_id = ""
            icon_name = ""
            
            for line in content:
                line = line.strip()
                if "URL=steam://rungameid/" in line:
                    game_id = line.split("/")[-1]
                elif "IconFile=" in line and line.lower().endswith(".ico"):
                    icon_name = os.path.basename(line)
                
                # Optimization: Early exit if both fields are found
                if game_id and icon_name:
                    break
            
            if game_id and icon_name:
                self._logger.info(f"Successfully parsed [{os.path.basename(file_path)}]: ID={game_id}, Icon={icon_name}")
                return SteamShortcut(
                    file_name=os.path.basename(file_path),
                    game_id=game_id,
                    icon_name=icon_name
                )
            else:
                self._logger.debug(f"Ignoring non-Steam or incomplete shortcut: {file_path}")
                
        except Exception as e:
            self._logger.error(f"Failed to parse file {file_path}: {str(e)}")
            
        return None
