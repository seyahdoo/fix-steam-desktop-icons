import logging
import os
from typing import List
from src.finder import WindowsSteamFinder
from src.provider import FileSystemShortcutProvider
from src.downloader import WebIconDownloader

class IconFixerService:
    """Service for coordinating the repair of Steam desktop icons."""

    def __init__(
        self,
        dir_finder: WindowsSteamFinder,
        shortcut_provider: FileSystemShortcutProvider,
        icon_downloader: WebIconDownloader
    ):
        self._dir_finder = dir_finder
        self._shortcut_provider = shortcut_provider
        self._icon_downloader = icon_downloader
        self._logger = logging.getLogger(__name__)

    def execute(self, desktop_paths: List[str]) -> None:
        """Execute the fix process."""
        self._logger.info(f"Analyzing desktop paths: {desktop_paths}")
        
        shortcuts = self._shortcut_provider.get_shortcuts(desktop_paths)
        if not shortcuts:
            self._logger.info("No Steam shortcuts found to fix.")
            return

        try:
            steam_base_dir = self._dir_finder.find_steam_install_path()
            game_icons_directory = os.path.join(steam_base_dir, "steam", "games")
            
            self._logger.info(f"Located Steam icon directory: {game_icons_directory}")
            if not os.path.exists(game_icons_directory):
                self._logger.info(f"Icon directory missing, creating: {game_icons_directory}")
                os.makedirs(game_icons_directory)

            existing_icons = set(os.listdir(game_icons_directory))
            
            for shortcut in shortcuts:
                # Get game name from file name without extension
                game_name = os.path.splitext(shortcut.file_name)[0]
                
                if shortcut.icon_name not in existing_icons:
                    self._logger.info(
                        f"Missing icon, downloading: {shortcut.icon_name} "
                        f"(Game ID: {shortcut.game_id}) (Game Name: {game_name})"
                    )
                    success = self._icon_downloader.download_icon(
                        shortcut.game_id, 
                        shortcut.icon_name, 
                        game_icons_directory
                    )
                    if success:
                        self._logger.info(f"Download successful: {shortcut.icon_name}")
                else:
                    self._logger.debug(f"Icon already exists, skipping: {shortcut.icon_name} (Game Name: {game_name})")
                
                # Output a blank line to group logs for this icon check/download
                print("")

        except Exception as e:
            self._logger.critical(f"Unexpected error during repair process: {str(e)}")
            raise
