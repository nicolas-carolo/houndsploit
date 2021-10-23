import subprocess
from datetime import datetime
import os
import platform
import time


def install_updates():
    """
    Run the script for making the pull of HoundSploit and exploitdb repositories.
    This script also manages the necessary files for hsploit.
    """
    store_copy_previous_csv_files()
    store_copy_previous_db_file()
    if platform.system() == "Windows":
        installer_path = os.path.expanduser("~") + "\.HoundSploit\houndsploit\\"
    else:
        installer_path = os.path.expanduser("~") + "/.HoundSploit/houndsploit/"
    if platform.system() == "Darwin":
        os.system(installer_path + "install_db_darwin.sh")
    elif platform.system() == "Linux":
        os.system(installer_path + "install_db_linux.sh")
    elif platform.system() == "Windows":
        os.system("powershell.exe -ExecutionPolicy Bypass -File " + installer_path + "install_db_windows.ps1")
    else:
        printf("ERROR: System not supported")


def migrate_to_new_installation():
    """
    Run the script for making the pull of Houndsploit and exploitdb repositories from the
    base directory of the previous installations in order to migrate to the new base path
    """
    installer_path = os.path.expanduser("~") + "/HoundSploit/houndsploit/"
    if platform.system() == "Darwin":
        os.system(installer_path + "install_db_darwin.sh")
    elif platform.system() == "Linux":
        os.system(installer_path + "install_db_linux.sh")
    elif platform.system() == "Windows":
        printf("Before running HoundSploit, follow the installation procedure!")
    else:
        printf("ERROR: System not supported")


def get_latest_db_update_date():
    """
    Get the date of the latest commit of the exploitdb database.
    :return: the date of the latest commit of the exploitdb database.
    """
    if platform.system() == "Windows":
        exploitdb_path = os.path.expanduser("~") + "\.HoundSploit\exploitdb"
    else:
        exploitdb_path = os.path.expanduser("~") + "/.HoundSploit/exploitdb"
    date_latest_db_update = subprocess.check_output("git -C " + exploitdb_path + " log -1 --format='%at'", shell=True)
    if platform.system() == "Windows":
        date_latest_db_update = int(date_latest_db_update.decode("utf-8")[1:-2])
    else:
        date_latest_db_update = int(date_latest_db_update.decode("utf-8"))
    return time.strftime('%Y-%m-%d', time.localtime(date_latest_db_update))


def store_copy_previous_csv_files():
    if platform.system() == "Windows":
        exploitdb_path = os.path.expanduser("~") + "\.HoundSploit\exploitdb\\"
        houndsploit_path = os.path.expanduser("~") + "\.HoundSploit\\"
    else:
        exploitdb_path = os.path.expanduser("~") + "/.HoundSploit/exploitdb/"
        houndsploit_path = os.path.expanduser("~") + "/.HoundSploit/"
    subprocess.check_output("cp " + exploitdb_path + "files_shellcodes.csv " + houndsploit_path + "old_file_shellcodes.csv", shell=True)
    subprocess.check_output("cp " + exploitdb_path + "files_exploits.csv " + houndsploit_path + "old_file_exploits.csv", shell=True)


def store_copy_previous_db_file():
    if platform.system() == "Windows":
        houndsploit_path = os.path.expanduser("~") + "\.HoundSploit\\"
    else:
        houndsploit_path = os.path.expanduser("~") + "/.HoundSploit/"
    subprocess.check_output("cp " + houndsploit_path + "hound_db.sqlite3 " + houndsploit_path + "fixed_hound_db.sqlite3", shell=True)