import os
import subprocess
from datetime import date
import shutil
import argparse

def get_newest_or_oldest_folder(BACKUP_PARENT, newest = True):
    folders = os.listdir(path = BACKUP_PARENT)
    folders.sort(reverse=newest)
    # newest or latest folder is 0
    # all fodlers is 1 
    return folders[0], folders

def do_backup(BACKUP_PARENT,SOURCE, MAX_NUM_BACKUPS,todays_date,dryrun):
    save_folder = f"backup_{todays_date}"
    if not save_folder in os.listdir(BACKUP_PARENT):
        os.mkdir(BACKUP_PARENT + save_folder) 

    delfolders = get_newest_or_oldest_folder(BACKUP_PARENT,False)
    print(delfolders)

    # edit flags and exclude rules here
    cmd = [
        "rsync",
        "-av", 
        "--dry-run" if dryrun else "",
        "--progress", 
        "--delete", 
        "--delete-excluded", 
        "--include", ".cache/",
        "--include", ".cache/mozilla/***",
        "--exclude", "Games/***",
        "--exclude", ".cache/***", 
        "--exclude", ".steam/***", 
        "--exclude", ".local/share/Steam/***", 
        SOURCE, 
        BACKUP_PARENT + save_folder
        ]

    cmd = [arg for arg in cmd if arg]

    if len(delfolders[1]) > MAX_NUM_BACKUPS:
        # first delete the oldest backup

        delfolder = delfolders[0]
        print(f"Folder for deletion: {delfolder}")
        shutil.rmtree(BACKUP_PARENT + delfolder)
        print(f"path removed {BACKUP_PARENT + delfolder}")

        #backup
        result = subprocess.run(cmd)
        print(result.stdout)  # command output
        print(result.stderr)  # error output, if any
        print(result.returncode)  # exit code 

        if dryrun:
            print("This was a dry run, no back up was completed! Add the --live flag to backup")
        else:
            print(f"backup completed at {BACKUP_PARENT + save_folder}")

    else:
        # backup
        result = subprocess.run(cmd)
        print(result.stdout)  # command output
        print(result.stderr)  # error output, if any
        print(result.returncode)  # exit code 

        if dryrun:
            print("This was a dry run, no back up was completed! Add the --live flag to backup")
        else:
            print(f"backup completed at {BACKUP_PARENT + save_folder}")

def main():
    parser = argparse.ArgumentParser(
    prog="simple python rsync backup",
    description="a simple programme to create backups at your chosen location"
    )
    
    parser.add_argument("--maxbackups", type = int , default = 5)
    parser.add_argument("--source", type = str)
    parser.add_argument("--dest", type = str)
    parser.add_argument("--live",action='store_true')
    args = parser.parse_args()

    MAX_NUM_BACKUPS = args.maxbackups
    BACKUP_PARENT = args.dest
    SOURCE = args.source
    dryrun = not args.live

    todays_date = date.today().strftime("%Y-%m-%d")

    if not os.path.isdir(BACKUP_PARENT):
       print(f"backup path does not exist please create or mount a backup folder at {BACKUP_PARENT}")
       exit()

    do_backup(BACKUP_PARENT,SOURCE,MAX_NUM_BACKUPS,todays_date,dryrun)

    
if __name__ == "__main__":
    main()
