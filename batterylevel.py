import subprocess
import os
import argparse


def cleanup_output(raw_output):
    clean_output = raw_output.replace("b","").replace("\\n","").replace("'","")
    return clean_output

def get_batteries_info():
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
    return batteries

def create_output(batteries_info):
    output=[]
    for bat in batteries_info:
            if bat["status"] == "Discharging" or bat["status"] == "Not charging":
                # icon picking formula
                icon = icons_colors[int(bat['perc']/10)]
            else:
                icon = f"{white}{icons[10]}"
            output.append(f"{icon} {bat['name']}:{bat['perc']}%")
    return " ".join(output)

def main():
    parser = argparse.ArgumentParser(
    prog="Battery levels simple script",
    description="reads the hwmon sys files to detect batteries input and outputs battery levels"
    )

    parser.add_argument("--icons",action='store_true')
    parser.add_argument("--no-icons",dest='icons',action='store_false')
    parser.add_argument("--colors",action='store_true')
    parser.add_argument("--no-colors",dest='colors',action='store_false')
    parser.set_defaults(icons=True,colors=True)
    args = parser.parse_args()


    if args.colors:
        green="^c#409960^"
        amber="^c#998240^"
        red="^c#ba1818^"
        white="^c#f2faf4^"
    else:
        green=""
        amber=""
        red=""
        white=""

    # icon at index 10 is used when the battery is charging
    if args.icons:
        icons = ["󰁺","󰁻","󰁼","󰁽","󰁾","󰁿","󰂀","󰂁","󰂂","󱟢","󰂄"]
    else:
        icons = ["","","","","","","","","","",""]

    # icons[10] is not included in icons_colors on purpose because
    # icons_colors needs to be 10 long (see icon picking formula below)
    icons_colors = [
        red+icons[0],
        red+icons[1],
        red+icons[2],
        amber+icons[3],
        amber+icons[4],
        amber+icons[5],
        green+icons[6],
        green+icons[7],
        green+icons[8],
        green+icons[9]
        ]

    batteries_info = get_batteries_info()
    output = create_output(batteries_info)

    print(output)


if __name__ == "__main__":
    main()