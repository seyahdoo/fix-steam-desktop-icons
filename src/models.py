from dataclasses import dataclass

@dataclass(frozen=True)
class SteamShortcut:
    """Entity class for Steam game desktop shortcuts."""
    file_name: str
    game_id: str
    icon_name: str
