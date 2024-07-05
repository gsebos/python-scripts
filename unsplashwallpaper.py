#!/usr/bin/env python3

import requests
import json
import subprocess
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

with open(f"{BASE_DIR}/api_key.txt","r") as f:
    for line in f:
        apikey=line

API_KEY = apikey.rstrip()
BASE_URL = "https://api.unsplash.com/photos/random"
WALLPAPER_PATH = "/home/seb/Pictures/Wallpapers/unsplash"

UNSPLASH_PARAMS = {
    "client_id" : API_KEY,
    "collections" : "1053828"
}

request = requests.get(BASE_URL,params=UNSPLASH_PARAMS)
jsonrequest = json.loads(request.content)
pictureurl = jsonrequest["urls"]["full"]

img_request = requests.get(pictureurl)

with open(f"{WALLPAPER_PATH}/wallpaper.jpg","bw") as img:
    img.write(img_request.content)

subprocess.run(["pkill","swaybg"])
subprocess.run(["/usr/bin/swaybg", "-i", WALLPAPER_PATH+"/wallpaper.jpg"])
