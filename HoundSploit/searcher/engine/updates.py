import subprocess
import shutil
import os
import platform
import time
from datetime import datetime
from HoundSploit.searcher.utils.constants import BASE_DIR, EXPLOITDB_PATH
from HoundSploit.searcher.utils.file import check_file_existence


INSTALLER_CMD = {
    "Darwin": BASE_DIR + "houndsploit/install_db_darwin.sh",
    "Linux": BASE_DIR + "houndsploit/install_db_linux.sh",
    "Windows": "powershell.exe -ExecutionPolicy Bypass -File " + BASE_DIR + "houndsploit/install_db_windows.ps1"
}
    

def install_updates():
    operating_system = platform.system()
    try:
        installer_command = INSTALLER_CMD[operating_system]
        os.system(installer_command)
    except KeyError:
        printf("ERROR: System not supported")
        exit(1)


def get_last_db_update_date():
    operating_system = platform.system()
    exploitdb_path = EXPLOITDB_PATH
    date_latest_db_update = subprocess.check_output("git -C " + exploitdb_path + " log -1 --format='%at'", shell=True)
    if operating_system == "Windows":
        date_latest_db_update = int(date_latest_db_update.decode("utf-8")[1:-2])
    else:
        date_latest_db_update = int(date_latest_db_update.decode("utf-8"))
    return time.strftime('%Y-%m-%d', time.localtime(date_latest_db_update))


def check_db_changes():
    if check_file_existence(BASE_DIR + "/houndsploit_db.lock"):
        if check_file_existence(BASE_DIR + "/hound_db.sqlite3"):
            os.remove(BASE_DIR + "/hound_db.sqlite3")
        create_db()
        db_update_alert = True
    else:
        db_update_alert = False
    return db_update_alert


def check_software_changes():
    if check_file_existence(BASE_DIR + "/houndsploit_sw.lock"):
        sw_update_alert = True
    else:
        sw_update_alert = False
    return sw_update_alert


def check_no_updates(db_update_alert, sw_update_alert):
    if sw_update_alert == False and db_update_alert == False:
        return True
    else:
        return False
