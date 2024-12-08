

import os

import urllib.request





games_directory = "C:\Program Files (x86)\Steam\steam\games"

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 

id_icons = []

for filename in os.listdir(desktop):
    if filename.endswith(".url"):
        with open(os.path.join(desktop, filename)) as f:
            lines = f.readlines()
        icon_name = ""
        game_id = ""
        for line in lines:
            line = line.strip()
            if line.endswith(".ico"):
                icon_name = line.split("\\")[-1]
            if "rungameid" in line:
                game_id = line.split("/")[-1]
        id_icons.append((game_id, icon_name))
        print(f"{game_id} {icon_name}")



filenames = os.listdir(games_directory)


for id_icon in id_icons:
    if not id_icon[1] in filenames:
        print(f"downloading {id_icon[0]} {id_icon[1]}")
        imgURL = f"https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/{id_icon[0]}/{id_icon[1]}"
        urllib.request.urlretrieve(imgURL, os.path.join(games_directory, id_icon[1]))

print("done!")

