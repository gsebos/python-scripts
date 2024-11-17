#!/usr/bin/env python3

import requests
import json
import subprocess
import os
import argparse
import shutil

class WallpaperManager:
    def __init__(self,collection,wallpaper_setter):
        self.USER = os.getlogin()
        self.BASE_DIR = os.path.dirname(os.path.realpath(__file__))
        self.API_KEY = self.get_api_key_from_file()
        self.BASE_URL = "https://api.unsplash.com/photos/random"
        self.WALLPAPER_PATH = f"/home/{self.USER}/Pictures/Wallpapers"
        self.DIRS_IN_PATH = os.listdir(f"{self.WALLPAPER_PATH}")
        self.num_monitors = len(self.monitors)
        self.COLLECTION = collection
        self.SETTER = wallpaper_setter
        self.UNSPLASH_PARAMS = {
                "client_id" : self.API_KEY,
                "collections" : self.COLLECTION
            }
        self.create_folders()
        self.download_wallpapers_from_unsplash()
    
    # Check if a folder was created by this app
    def is_app_folder(self, dir):
        if os.path.isdir(f"{self.WALLPAPER_PATH}/{dir}") and dir.startswith("uws_mon"):
            return True
        else:
            return False
        
    @property
    def monitors(self):
        self._monitors = []
        monitors = str(subprocess.check_output("xrandr --listactivemonitors  | awk '{print $4}'",shell=True))
        for mon in monitors.split("\\n"):
            self._monitors.append(mon)
        return self._monitors[1:-1]

    @property 
    def MONITORS_FOLDER(self):
        self._MONITORS_FOLDERS = []      
        for dir in self.DIRS_IN_PATH:
            if self.is_app_folder(dir):
                self._MONITORS_FOLDERS.append(f"{self.WALLPAPER_PATH}/{dir}")
        return self._MONITORS_FOLDERS

    @classmethod
    def is_session_wayland(cls):
        session_type = os.environ['XDG_SESSION_TYPE']
        if session_type == "wayland":
            return True
        else:
            return False


    def create_folders(self):
            # remove existing folders in case number of screen has changed 
            for dir in self.DIRS_IN_PATH:
                if self.is_app_folder(dir):
                    shutil.rmtree(f"{self.WALLPAPER_PATH}/{dir}")  
            # Then create new folders
            for i in range(self.num_monitors):
                if not os.path.exists(f"{self.WALLPAPER_PATH}/uws_mon{i}"):
                    os.makedirs(f"{self.WALLPAPER_PATH}/uws_mon{i}")

    def get_api_key_from_file(self):
        with open(f"{self.BASE_DIR}/api_key.txt","r") as f:
            for line in f:
                apikey=line
        return apikey.rstrip()


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
            settercmd = []
            if self.SETTER == "swaybg":
                settercmd = [self.SETTER,"-i",f"{mon}/wallpaper.jpg"]
            else:
                settercmd = [self.SETTER]  
            subprocess.run(["pkill",self.SETTER])
            subprocess.run([*settercmd])
        else:
            subprocess.run(["pkill","feh"])
            subprocess.run(["feh", *wallpapercmd])

class wpaperdConfig:
    def __init__(self,wallpaper_dirs_path,monitors):
        self.CONFIG_PATH = f"/home/{os.getlogin()}/.config/wpaperd/"
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
        if os.path.exists(self.CONFIG_PATH) and WallpaperManager.is_session_wayland():
            with open(f"{self.CONFIG_PATH}wallpaper.toml",'w') as f:
                    f.writelines(self.create_config())
        

def main():
    parser = argparse.ArgumentParser(
    prog="Random Unsplash Wallpaper",
    description="Uses the unsplash API to fetch a random image and set it as wallpaper using feh (X11) or a choice of wpaperd(default) or swaybg in wayland",
    epilog="Dependencies: feh, xrandr, wpaperd or swaybg, pip requests"
)
    parser.add_argument("--collection",type=str, default="1053828",help="the unsplash collection id")
    parser.add_argument("--waylandsetter",choices=["swaybg","wpaperd"],default="wpaperd")
    args = parser.parse_args()

    manager = WallpaperManager(args.collection, args.waylandsetter)
    # create config for wpaperd use

    config = wpaperdConfig(manager.MONITORS_FOLDER,manager.monitors)
    print(f"wrote config file:\n {config.config}")
    
    # Saves .config/wpaperd/wallpaper.toml with detected monitors
    config.save_config()
    
    # output to terminal for debugging
    print(f"num monitors: {manager.num_monitors}")
    


    # Set wallpaper test
    manager.set_wallpapers()

if __name__ == "__main__":
    main()