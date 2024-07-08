#!/usr/bin/env python3

import requests
import json
import subprocess
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--collections",type=str, default="1053828")
# parser.add_argument("--mode",type=int,default=2)
parser.add_argument("--waylandsetter",choices=["swaybg","wpaperd"],default="wpaperd")
args = parser.parse_args()

class WallpaperManager:
    def __init__(self,collections=args.collections):
        self.USER = os.getlogin()
        self.BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        self.API_KEY = self.get_api_key_from_file()
        self.BASE_URL = "https://api.unsplash.com/photos/random"
        self.WALLPAPER_PATH = f"/home/{self.USER}/Pictures/Wallpapers"
        self.num_monitors = len(self.monitors)
        self.COLLECTIONS = collections
        self.UNSPLASH_PARAMS = {
                "client_id" : self.API_KEY,
                "collections" : self.COLLECTIONS
            }
        self.create_folders()
        self.download_wallpapers_from_unsplash()
    
    @property
    def monitors(self):
        self._monitors = []
        monitors = str(subprocess.check_output("xrandr --listactivemonitors  | awk '{print $4}'",shell=True))
        for mon in monitors.split("\\n"):
            self._monitors.append(mon)
        return self._monitors[1:-1]

    @property 
    def MONITORS_FOLDER(self):
        dirs = os.listdir(f"{self.WALLPAPER_PATH}")
        self._MONITORS_FOLDERS = []
        for dir in dirs:
            if os.path.isdir(f"{self.WALLPAPER_PATH}/{dir}") and dir.startswith("uws_mon"):
                self._MONITORS_FOLDERS.append(f"{self.WALLPAPER_PATH}/{dir}")
        return self._MONITORS_FOLDERS

    def create_folders(self):
            for i in range(self.num_monitors):
                if not os.path.exists(f"{self.WALLPAPER_PATH}/uws_mon{i}"):
                    os.makedirs(f"{self.WALLPAPER_PATH}/uws_mon{i}")

    def get_api_key_from_file(self):
        with open(f"{self.BASE_DIR}/api_key.txt","r") as f:
            for line in f:
                apikey=line
        return apikey.rstrip()

    def is_session_wayland(self):
        session_type = os.environ['XDG_SESSION_TYPE']
        if session_type == "wayland":
            return True
        else:
            return False

    def download_wallpapers_from_unsplash(self):
        wallpapers = []
        print(self.MONITORS_FOLDER)
        for mon in self.MONITORS_FOLDER:
            request = requests.get(self.BASE_URL,self.UNSPLASH_PARAMS)
            print(request)
            jsonrequest = json.loads(request.content)
            pictureurl = jsonrequest["urls"]["full"]
            img_request = requests.get(pictureurl)

            with open(f"{mon}/wallpaper.jpg","bw") as img:
                img.write(img_request.content)


    def set_wallpapers(self):
        wallpapers = self.MONITORS_FOLDER
        wallpapercmd = []
        for mon in wallpapers:
            wallpapercmd.append("--bg-fill")
            wallpapercmd.append(mon)

        if self.is_session_wayland():
                subprocess.run(["pkill",args.waylandsetter])
                subprocess.run([args.waylandsetter])
        else:
            subprocess.run(["pkill","feh"])
            subprocess.run(["feh", *wallpapercmd])

class wpaperdConfig:
    def __init__(self,wallpaper_dirs_path,monitors):
        self.CONFIG_PATH = f"/home/{os.getlogin()}/.config/wpaperd/wallpaper.toml"
        self.wallpaper_dirs_path = wallpaper_dirs_path
        self.monitors = monitors
        self.create_config()
        
    def create_config(self):
        self.config = []
        for i,line in enumerate(self.wallpaper_dirs_path):
                self.config.append(f"[{self.monitors[i]}]\n")
                self.config.append(f'path = "{line}"\n')
                self.config.append("apply-shadow = true\n")
                self.config.append("\n")
        return self.config

    def save_config(self):
        with open(self.CONFIG_PATH,'w') as f:
                f.writelines(self.create_config())
        

def main():
    manager = WallpaperManager()

    # create config for wpaperd use
    config = wpaperdConfig(manager.MONITORS_FOLDER,manager.monitors)

    # output to terminal for debugging
    print(f"wrote config file:\n {config.config}")
    print(f"num monitors: {manager.num_monitors}")
    
    # Saves .config/wpaperd/wallpaper.toml with detected monitors
    config.save_config()

    # Set wallpaper
    manager.set_wallpapers()

if __name__ == "__main__":
    main()