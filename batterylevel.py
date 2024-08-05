import subprocess
import os
import argparse


class Battery():
    def __init__(self,use_colors:bool,use_icons:bool):
        self.batteries_info = self.get_batteries_info()
        if use_colors:
            self.colors = {
            "green": "^c#409960^",
            "amber":"^c#998240^",
            "red":"^c#ba1818^",
            "white":"^c#f2faf4^"
            }
        else:
            self.colors = {
            "green": "",
            "amber":"",
            "red":"",
            "white":""
            }

        # icon at index 10 is used when the battery is charging
        if use_icons:
            self.icons = ["󰁺","󰁻","󰁼","󰁽","󰁾","󰁿","󰂀","󰂁","󰂂","󱟢","󰂄"]
        else:
            self.icons = ["","","","","","","","","","",""]

        # self.icons[10] is not included in icons_colors on purpose because
        # self.icons_colors needs to be 10 long (see icon picking formula below)
        self.icons_colors = [
            self.colors["red"]+self.icons[0],
            self.colors["red"]+self.icons[1],
            self.colors["red"]+self.icons[2],
            self.colors["amber"]+self.icons[3],
            self.colors["amber"]+self.icons[4],
            self.colors["amber"]+self.icons[5],
            self.colors["green"]+self.icons[6],
            self.colors["green"]+self.icons[7],
            self.colors["green"]+self.icons[8],
            self.colors["green"]+self.icons[9]
            ]
        

    def cleanup_output(self,raw_output):
        clean_output = raw_output.replace("b","").replace("\\n","").replace("'","")
        return clean_output

    def get_batteries_info(self):
        batteries = []
        for file in os.listdir('/sys/class/hwmon/'):
            dev_name = self.cleanup_output(str(subprocess.check_output(f"cat /sys/class/hwmon/{file}/name", shell=True)))
            if "BAT" in dev_name:
                bat = {}
                bat["name"]= dev_name
                bat["status"]= self.cleanup_output(str(subprocess.check_output(f"cat /sys/class/hwmon/{file}/device/status", shell=True)))
                bat["full"]=int(subprocess.check_output(f"cat /sys/class/hwmon/{file}/device/energy_full", shell=True))
                bat["now"]=int(subprocess.check_output(f"cat /sys/class/hwmon/{file}/device/energy_now", shell=True))
                bat["perc"] = round((bat["now"] / bat["full"])*100)
                batteries.append(bat)
        return batteries

    def create_output(self):
        output=[]
        for bat in self.batteries_info:
                if bat["status"] == "Discharging" or bat["status"] == "Not charging":
                    # icon picking formula
                    icon = self.icons_colors[int(bat['perc']/10)]
                else:
                    icon = f"{self.colors['white']}{self.icons[10]}"
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


    battery = Battery(args.colors, args.icons)
    print(battery.create_output())


if __name__ == "__main__":
    main()