import subprocess
from datetime import datetime
import os
import platform
import time


def install_updates():
    """
    Run the script for making the pull of hsploit and exploitdb repositories.
    This script also manages the necessary files for hsploit.
    """
    installer_path = os.path.expanduser("~") + "/HoundSploit/houndsploit/"
    if platform.system() == "Darwin":
        os.system(installer_path + "install_db_darwin.sh")
    elif platform.system() == "Linux":
        os.system(installer_path + "install_db_linux.sh")
    else:
        printf("ERROR: System not supported")


def get_latest_db_update_date():
    """
    Get the date of the latest commit of the exploitdb database.
    :return: the date of the latest commit of the exploitdb database.
    """
    exploitdb_path = os.path.expanduser("~") + "/HoundSploit/exploitdb"
    date_latest_db_update = subprocess.check_output("git -C " + exploitdb_path + " log -1 --format='%at'", shell=True)
    date_latest_db_update = int(date_latest_db_update.decode("utf-8"))
    return time.strftime('%Y-%m-%d', time.localtime(date_latest_db_update))