import os
import subprocess
from datetime import date
import shutil
import argparse

def get_newest_or_oldest_folder(BACKUP_PARENT, mode, PREFIX):
    if mode not in ("newest","oldest"):
         raise ValueError("mode must be either 'newest' or 'oldest'")
    
    folders = os.listdir(path = BACKUP_PARENT)
    folders.sort(reverse = (mode == "newest"))

    backup_folders = [ folder for folder in folders if os.path.isdir( BACKUP_PARENT + folder) and folder.startswith(PREFIX) ]

    return backup_folders[0], backup_folders

def do_backup(BACKUP_PARENT,SOURCE, MAX_NUM_BACKUPS,todays_date,dryrun, PREFIX):
    # make sure the backup folder exists, if not create it
    save_folder = f"{PREFIX}_{todays_date}"
    if not save_folder in os.listdir(BACKUP_PARENT):
        os.mkdir(BACKUP_PARENT + save_folder) 

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
        "--exclude", "Zomboid/***", 
        "--exclude", ".local/share/Steam/***", 
        SOURCE, 
        BACKUP_PARENT + save_folder
        ]
    # remove any empty argument 
    cmd = [arg for arg in cmd if arg]

    print(f"######### back up {todays_date} #########" )

    # get the oldest backup folder and the list of backup folders already present
    oldest_folder, folders = get_newest_or_oldest_folder(BACKUP_PARENT,"oldest", PREFIX)

    if len(folders) > MAX_NUM_BACKUPS:
        # first delete the oldest backup
        print(f"Folder for deletion: {oldest_folder}")
        shutil.rmtree(BACKUP_PARENT + oldest_folder)
        print(f"path removed {BACKUP_PARENT + oldest_folder}")
        # then backup  
        result = subprocess.run(cmd)

    else:
        # just backup
        result = subprocess.run(cmd)
    
    print(f"exit code: {result.returncode}")  # exit code 

    if dryrun:
        print("[WARNING] This was a dry run, no back up was completed! Add the --live flag to backup")
        print(f"[INFO] Source would be {SOURCE}")
        print(f"[INFO] destination would be {BACKUP_PARENT + save_folder}")
    else:
        print(f"[INFO] Backup completed at {BACKUP_PARENT + save_folder}")

def main():
    parser = argparse.ArgumentParser(
    prog="python backup.py",
    description="a simple programme to create backups using rsync"
    )
    
    parser.add_argument("--maxbackups", type = int , default = 5, help="when limit is reached, oldest foler is overwritten")
    parser.add_argument("--source", type = str , default = "/home/seb/",help="default is /home/seb/")
    parser.add_argument("--prefix", type = str , default = "ez-rsync-backup",help="default is backup")
    parser.add_argument("--dest", type = str , default = "/mnt/casita-share/pc_backups/", help="default is /mnt/casita-share/pc_backups/")
    parser.add_argument("--live",action='store_true', help="if not present rsync runs in dry run mode")
    args = parser.parse_args()

    MAX_NUM_BACKUPS = args.maxbackups
    BACKUP_PARENT = args.dest
    SOURCE = args.source
    PREFIX = args.prefix
    dryrun = not args.live

    todays_date = date.today().strftime("%Y-%m-%d")

    errors = []

    if not os.path.isdir(BACKUP_PARENT):
       errors.append(f"[WARNING] Backup containing folder path {BACKUP_PARENT} does not exist, define it with the --dest flag")
       
    if not os.path.isdir(SOURCE):
        errors.append(f"[WARNING] Backup source path {SOURCE} does not exist, define it with the --source flag")
    
    if errors:
        for error in errors:
            print(error)
        exit()
    
    do_backup(BACKUP_PARENT,SOURCE,MAX_NUM_BACKUPS,todays_date,dryrun, PREFIX)
   
    
if __name__ == "__main__":
    main()
