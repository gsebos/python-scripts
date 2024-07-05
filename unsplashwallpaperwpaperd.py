#!/usr/bin/env python3

import requests
import json
import subprocess
import os

USER = os.getlogin()
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(f"{BASE_DIR}/api_key.txt","r") as f:
    for line in f:
        apikey=line

API_KEY = apikey.rstrip()
BASE_URL = "https://api.unsplash.com/photos/random"
WALLPAPER_PATH = f"/home/{USER}/Pictures/Wallpapers"
MONITORS_FOLDER = ("rightmon","leftmon")
UNSPLASH_PARAMS = {
        "client_id" : API_KEY,
        "collections" : "1053828"
    }

for mon in MONITORS_FOLDER:
    request = requests.get(BASE_URL,params=UNSPLASH_PARAMS)
    print(request)
    jsonrequest = json.loads(request.content)
    pictureurl = jsonrequest["urls"]["full"]

    img_request = requests.get(pictureurl)

    with open(f"{WALLPAPER_PATH}/{mon}/wallpaper.jpg","bw") as img:
        img.write(img_request.content)

    

subprocess.run(["pkill","waperd"])
subprocess.run(["wpaperd"])
