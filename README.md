# Random Unsplash wallpaper on demand

A quick script to get a random unsplash picture as wallpaper in linux. This uses feh for X11 and wpaperd for wayland so these two programmes need to be installed on the system for this to work.

clone the repo:
`git clone https://github.com/gsebos/python-scripts.git`
then cd into it

## For use with swaybg - unsplashwallpaper.py -(1 monitor)

1. Get an api key from [https://unsplash.com/documentation](https://unsplash.com/documentation)
2. Save the key in a file named `api_key.txt` **in the same folder as the scripts, i.e. inside the python_scripts folder** 
3. Install `swaybg` using your package manager 
4. Install the python module `requests` using `pip` [in a venv](https://docs.python.org/3/library/venv.html) or with your preferred method
5. Make sure that you have the following folder structure `/home/{USER}/Pictures/Wallpapers/unsplash` or change the variable `WALLPAPER_PATH` (no trailing `/` at the end) if you want to store your wallpaper somewhere else.

run script in command line or bind keys in your DE/WM.

## For use with wpaperd - unsplas-hwallpaper-dual.py - (2 or more monitors)

1. Get an api key from [https://unsplash.com/documentation](https://unsplash.com/documentation)
2. Save the key in a file named `api_key.txt` **in the same folder as the scripts, i.e. inside the python_scripts folder** 
3. Install `wpaperd` using your package manager 
4. Install the python module `requests` using `pip` [in a venv](https://docs.python.org/3/library/venv.html) or with your preferred method
5. Make sure that you have the following folder structure `/home/{USER}/Pictures/Wallpapers` and add a `rightmon` and a `leftmon` folder.
In other words, you should have these two folders:
- `/home/{USER}/Pictures/Wallpapers/rightmon`  
- `/home/{USER}/Pictures/Wallpapers/leftmon`

### wpaperd configuration (Feh shoud not require any configuration to work with this script)

Edit the wpaperd configuration at `~/.config/wpaperd/wallpaper.toml` as below
- replace `your_user_name` with your actual user name
- change the monitor headers to your own

```
# To set fallback wallpapers
[default] 
path = "/home/seb/Pictures/Wallpapers/"
duration = "30m"
sorting = "ascending"

# Check your WM or DE on how to check monitor id
[DP-2]
path = "/home/your_user_name/Pictures/Wallpapers/rightmon"
duration = "30m"
sorting = "descending"
apply-shadow = true

[HDMI-A-1]
path = "/home/your_user_name/Pictures/Wallpapers/leftmon"                                                    
duration = "30m"
sorting = "descending"
apply-shadow = true

```

run script in command line or bind keys in your DE/WM.

~### Adding more monitors~ TAKEN OUT MOMENTARILY

1. Create a folder for the extra monitor inside `~/Pictures/Wallpapers`, here called `your_extra_monitor` for example
2. Add the folder name to the variable MONITORS_FOLDER (e.g. `MONITORS_FOLDER = ("rightmon","leftmon","your_extra_monitor")`)
3. Add an entry to the `wallpaper.toml file`. 

```
[YOU_EXTRA_MONITOR_ID]
path = "/home/your_user_name/Pictures/Wallpapers/your_extra_monitor"                                                    
duration = "30m"
sorting = "descending"
apply-shadow = true
```
