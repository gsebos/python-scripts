import subprocess
import os
import argparse

parser = argparse.ArgumentParser(
    prog="Battery levels simple script",
    description="reads the hwmon sys files to detect batteries input and outputs battery levels"
)
parser.add_argument("--icons",type=bool,default=True)
parser.add_argument("--colors",type=bool,default=False)

# status2d colors
green="^c#409960^"
amber="^c#998240^"
red="^c#ba1818^"

icons = ["󰁺","󰁻","󰁼","󰁽","󰁾","󰁿","󰂀","󰂁","󰂂","󱟢"]
icons_colors = [red+"󰁺",red+"󰁻",red+"󰁼",amber+"󰁽",amber+"󰁾",amber+"󰁿",green+"󰂀",green+"󰂁",green+"󰂂",green+"󱟢"]

def cleanup_output(raw_output):
    clean_output = raw_output.replace("b","").replace("\\n","").replace("'","")
    return clean_output

batteries = []
for file in os.listdir('/sys/class/hwmon/'):
    dev_name = cleanup_output(str(subprocess.check_output(f"cat /sys/class/hwmon/{file}/name", shell=True)))
    if "BAT" in dev_name:
        bat = {}
        bat["name"]= dev_name
        bat["status"]= cleanup_output(str(subprocess.check_output(f"cat /sys/class/hwmon/{file}/device/status", shell=True)))
        bat["full"]=int(subprocess.check_output(f"cat /sys/class/hwmon/{file}/device/energy_full", shell=True))
        bat["now"]=int(subprocess.check_output(f"cat /sys/class/hwmon/{file}/device/energy_now", shell=True))
        bat["perc"] = round((bat["now"] / bat["full"])*100)
        batteries.append(bat)
batinfo=[]
for bat in batteries:
    if bat["status"] == "Discharging" or bat["status"] == "Not charging":
        icon = icons_colors[int(bat['perc']/10)]
    else:
        icon = "^c#f2faf4^󰂄"
    batinfo.append(f"{icon} {bat['name']}:{bat['perc']}%")

print(" ".join(batinfo))
print(batteries[0]["status"])