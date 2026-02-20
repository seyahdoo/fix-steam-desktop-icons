import logging
import sys
from src.service import IconFixerService
from src.finder import WindowsSteamFinder
from src.provider import FileSystemShortcutProvider
from src.downloader import WebIconDownloader
from src.config import DesktopConfigLoader

# Configure logging format and level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Main entry point of the application."""
    print("Steam Desktop Shortcut Icon Fixer v1.0.3\n")
    logger = logging.getLogger(__name__)

    try:
        try:
            # 1. Initialize dependencies
            dir_finder = WindowsSteamFinder()
            shortcut_provider = FileSystemShortcutProvider()
            icon_downloader = WebIconDownloader()
            config_loader = DesktopConfigLoader()

            # 2. Get desktop paths
            desktop_paths = config_loader.get_desktop_paths()
            if not desktop_paths:
                logger.error("No valid desktop paths found. Execution aborted.")
                return
            
            logger.info(f"Targeting desktop paths: {desktop_paths}")

            # 3. Initialize and execute application service
            service = IconFixerService(
                dir_finder=dir_finder,
                shortcut_provider=shortcut_provider,
                icon_downloader=icon_downloader
            )
            
            service.execute(desktop_paths)
            print("\neverything done! refresh desktop to load the icons.")

        except Exception as e:
            logger.critical(f"Critical error occurred during execution: {str(e)}", exc_info=True)
            print("\nan unrecognized error occurred while running the application.")
            print("check the log for details.")

    finally:
        print("\npress enter to exit...")
        input()

if __name__ == "__main__":
    main()
