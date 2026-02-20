import urllib.request
import os
import logging

class WebIconDownloader:
    """Implementation for downloading game icons via Steam CDN."""

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._base_url = "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps"

    def download_icon(self, game_id: str, icon_name: str, save_directory: str) -> bool:
        """Download and save icon from the web."""
        img_url = f"{self._base_url}/{game_id}/{icon_name}"
        save_path = os.path.join(save_directory, icon_name)
        
        try:
            self._logger.debug(f"Downloading from: {img_url}")
            self._logger.debug(f"Saving to: {save_path}")
            
            # Ensure the directory exists (redundant safety check)
            os.makedirs(save_directory, exist_ok=True)
            
            urllib.request.urlretrieve(img_url, save_path)
            return True
        except Exception as e:
            self._logger.error(f"Failed to download {icon_name}: {str(e)}")
            return False
