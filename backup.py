import os
import subprocess
from datetime import date
import shutil
import argparse
import getpass

def get_newest_or_oldest_folder(BACKUP_PARENT, mode, PREFIX):
    if mode not in ("newest","oldest"):
         raise ValueError("mode must be either 'newest' or 'oldest'")
    
    folders = os.listdir(path = BACKUP_PARENT)
    folders.sort(reverse = (mode == "newest"))

    backup_folders = [ folder for folder in folders if os.path.isdir( os.path.join(BACKUP_PARENT, folder)) and folder.startswith(PREFIX) ]

    return backup_folders[0], backup_folders

def build_cmd(FLAGS, dryrun, SOURCE, save_path, silent):
    flags = FLAGS.split(' ')
    option = "-a" if silent else "-av"
    
    cmd = ['rsync', "--progress" ,"--dry-run" if dryrun else "",SOURCE, save_path]
    cmd.insert(1,option)
    cmd[4:4] = flags

    # remove any empty argument 
    cmd = [arg for arg in cmd if arg]

    return cmd, ' '.join(cmd)


def do_backup(BACKUP_PARENT,SOURCE, MAX_NUM_BACKUPS,todays_date, command ,PREFIX):
    # make sure the backup folder exists, if not create it)
    save_folder = f"{PREFIX}_{todays_date}"
    if not save_folder in os.listdir(BACKUP_PARENT):
        os.mkdir(os.path.join(BACKUP_PARENT, save_folder)) 

    print(f"######### back up {todays_date} #########" )

    # get the oldest backup folder and the list of backup folders already present
    oldest_folder, folders = get_newest_or_oldest_folder(BACKUP_PARENT,"oldest", PREFIX)

    if len(folders) > MAX_NUM_BACKUPS:
        # first delete the oldest backup
        print(f"Folder for deletion: {oldest_folder}")
        shutil.rmtree(os.path.join(BACKUP_PARENT , oldest_folder))
        print(f"path removed {os.path.join(BACKUP_PARENT , oldest_folder)}")
        # then backup  
        result = subprocess.run(command)

    else:
        # just backup
        result = subprocess.run(command)
    
    print(f"exit code: {result.returncode}")  # exit code 
    print(f"[INFO] Backup completed at {os.path.join(BACKUP_PARENT, save_folder)}")

def main():
    user = getpass.getuser()
    parser = argparse.ArgumentParser(
    prog="python backup.py",
    description="""A simple programme to create backups using rsync and automates the backup rotation. 
    This creates a new folder everytime the programme runs. 
    The maximum number of folder is defined by the --maxbackups flag, default is 5 """
    )

    parser.add_argument("--maxbackups", type = int , default = 5, help="when limit is reached, oldest foler is overwritten")
    parser.add_argument("--source", type = str , default = f"/home/{user}/",help=f"default is /home/{user}/")
    parser.add_argument("--dest", type = str , default = "/mnt/casita-share/pc_backups/", help="default is /mnt/casita-share/pc_backups/")
    parser.add_argument("--flags", type = str , default = "--delete --delete-excluded --exclude Games/*** --exclude .cache/*** --exclude .steam/*** --exclude Zomboid/*** --exclude .local/share/Steam/***",help="flags space separated")
    parser.add_argument("--prefix", type = str , default = "pyrsync-backup",help="default is pyrsync-backup")
    parser.add_argument("--live",action='store_true', help="if not present rsync runs in dry run mode")
    parser.add_argument("--silent",action='store_true', help="no -v flag, runs without output")
    args = parser.parse_args()

    MAX_NUM_BACKUPS = args.maxbackups
    BACKUP_PARENT = args.dest
    SOURCE = os.path.join(args.source,'')
    PREFIX = args.prefix
    dryrun = not args.live
    flags = args.flags
    silent = args.silent

    todays_date = date.today().strftime("%Y-%m-%d")

    save_folder = PREFIX + '_' + todays_date
    save_path = os.path.join(BACKUP_PARENT, save_folder)

    errors = []

    if not os.path.isdir(BACKUP_PARENT):
       errors.append(f"[WARNING] Backup containing folder path {BACKUP_PARENT} does not exist, define it with the --dest flag")
       
    if not os.path.isdir(SOURCE):
        errors.append(f"[WARNING] Backup source path {SOURCE} does not exist, define it with the --source flag")
    
    if errors:
        for error in errors:
            print(error)
        exit()

    command = build_cmd(flags,dryrun, SOURCE, save_path, silent)

    print()
    print(f"[INFO] rsync command: {command[1]}")
    print()
    print("for help on how to change the rsync command, run python backup.py --help")
    print()

    if dryrun:
        print("[INFO] Running in dry-run mode...")
        print(f"[INFO] Source would be {SOURCE}")
        print(f"[INFO] destination would be {save_path}")  
        print()
        run_dryrun = input("Press any key to continue dryrun mode, q to exit. To run the back up, rerun the command with the --live flag\n")
        if run_dryrun == "q":
            print("programme exited")
            exit()
    else:
        confirm = input(f"You are about to back up the content of {SOURCE} into {save_path} (type yes to confirm)")

        if not confirm == "yes".lower():
            print("backup aborted")
            exit()

    do_backup(BACKUP_PARENT,SOURCE,MAX_NUM_BACKUPS,todays_date, command[0],PREFIX)
                
    
if __name__ == "__main__":
    main()
