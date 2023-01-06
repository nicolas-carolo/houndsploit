import os
from shutil import copyfile
from HoundSploit.searcher.utils.vulnerability import get_vulnerability_file_path


def check_file_existence(filename):
    try:
        f = open(filename)
        f.close()
        return True
    except IOError:
        return False 


def download_vulnerability_file(vulnerability):
    if vulnerability.type == "shellcode":
        vulnerability_class = "shellcode"
    else:
        vulnerability_class = "exploit"
    file_path = get_vulnerability_file_path(vulnerability)
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()
            vulnerability_code = ''.join(content)
        copyfile(file_path, os.path.expanduser("~") + "/" + vulnerability_class + "_" + vulnerability.id + vulnerability.get_extension())
        download_msg = vulnerability_class + "_" + vulnerability.id + vulnerability.get_extension() + " has been downloaded in your home directory"
        return True, download_msg
    except FileNotFoundError:
        error_msg = 'Sorry! This file does not exist :('
        return False, error_msg