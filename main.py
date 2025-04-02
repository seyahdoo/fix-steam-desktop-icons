import os
import urllib.request

def main():
    print("Steam Desktop Shortcut Icon Fixer v1.0.1")
    print("Toprak Seyyid Doğan")
    print("seyahdoo.com")
    print("............")
    print("............")
    print("............")

    print("analyzing desktop for steam url shortcuts")
    desktop_directory = os.path.join(os.path.join(os.environ["USERPROFILE"]), 'Desktop') 
    id_icon_names = []
    for filename in os.listdir(desktop_directory):
        if filename.endswith(".url"):
            id_icon = get_id_icon_names(os.path.join(desktop_directory, filename))
            if id_icon[0] and id_icon[1]:
                id_icon_names.append(id_icon)

    print("analyzing steam game icons directory and downloading missing icons")
    game_icons_directory = "C:\\Program Files (x86)\\Steam\\steam\\games"
    filenames = os.listdir(game_icons_directory)
    for id_icon in id_icon_names:
        if not id_icon[1] in filenames:
            print(f"downloading {id_icon[0]} {id_icon[1]}")
            imgURL = f"https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/{id_icon[0]}/{id_icon[1]}"
            urllib.request.urlretrieve(imgURL, os.path.join(game_icons_directory, id_icon[1]))

    print("everything done! refresh desktop to load the icons.")
    print("press enter to exit...")
    input()

def get_id_icon_names(path):
    lines = get_lines(path)
    icon_name = ""
    game_id = ""
    for line in lines:
        line = line.strip()
        if line.endswith(".ico"):
            icon_name = line.split("\\")[-1]
        if "rungameid" in line:
            game_id = line.split("/")[-1]
    return (game_id, icon_name)


def get_lines(path):
    with open(path) as f:
        return f.readlines()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        print("an unrecognized error occurred while running the application.")
        print("press enter to exit...")
        input()
