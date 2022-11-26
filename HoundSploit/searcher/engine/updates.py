import subprocess
import shutil
import os
import platform
import time
from datetime import datetime
from HoundSploit.searcher.utils.constants import BASE_PATH, EXPLOITDB_PATH


INSTALLER_CMD = {
    "Darwin": BASE_PATH + "houndsploit/install_db_darwin.sh",
    "Linux": BASE_PATH + "houndsploit/install_db_linux.sh",
    "Windows": "powershell.exe -ExecutionPolicy Bypass -File " + BASE_PATH + "houndsploit/install_db_windows.ps1"
}


def install_updates():
    store_copy_previous_csv_files()
    store_copy_previous_db_file()
    run_installer()
    

def run_installer():
    operating_system = platform.system()
    try:
        installer_command = INSTALLER_CMD[operating_system]
        os.system(installer_command)
    except KeyError:
        printf("ERROR: System not supported")
        exit(1)


def migrate_to_new_installation():
    run_installer()


def get_last_db_update_date():
    operating_system = platform.system()
    exploitdb_path = EXPLOITDB_PATH
    date_latest_db_update = subprocess.check_output("git -C " + exploitdb_path + " log -1 --format='%at'", shell=True)
    if operating_system == "Windows":
        date_latest_db_update = int(date_latest_db_update.decode("utf-8")[1:-2])
    else:
        date_latest_db_update = int(date_latest_db_update.decode("utf-8"))
    return time.strftime('%Y-%m-%d', time.localtime(date_latest_db_update))


def store_copy_previous_csv_files():
    exploitdb_path = EXPLOITDB_PATH
    houndsploit_path = BASE_PATH
    shutil.copyfile(os.path.abspath(exploitdb_path + "/files_shellcodes.csv"), os.path.abspath(houndsploit_path + "/old_files_shellcodes.csv"))
    shutil.copyfile(exploitdb_path + "/files_exploits.csv", houndsploit_path + "/old_files_exploits.csv")


def store_copy_previous_db_file():
    houndsploit_path = BASE_PATH
    shutil.copyfile(os.path.abspath(houndsploit_path + "/hound_db.sqlite3"), os.path.abspath(houndsploit_path + "/fixed_hound_db.sqlite3"))