import subprocess
import os
import platform
import csv
from distutils.dir_util import copy_tree
from HoundSploit.searcher.db_manager.models import Exploit, Shellcode
from HoundSploit.searcher.db_manager.session_manager import start_session

last_exploitdb_commit = '23acd8a13b7a871e735016897c7a9e7b0ac33448'


def fix_known_dates():
    if platform.system() == "Windows":
        exploitdb_path_src = os.path.expanduser("~") + "\.HoundSploit\exploitdb"
        exploitdb_path_dst = os.path.expanduser("~") + "\.HoundSploit\\fixed_exploitdb"
        exploits_path = exploitdb_path_dst + "\\files_exploits.csv"
        shellcodes_path = exploitdb_path_dst + "\\files_shellcodes.csv"
    else:
        exploitdb_path_src = os.path.expanduser("~") + "/.HoundSploit/exploitdb"
        exploitdb_path_dst = os.path.expanduser("~") + "/.HoundSploit/fixed_exploitdb"
        exploits_path = exploitdb_path_dst + "/files_exploits.csv"
        shellcodes_path = exploitdb_path_dst + "/files_shellcodes.csv"

    copy_tree(exploitdb_path_src, exploitdb_path_dst)
    subprocess.check_output("git -C " + exploitdb_path_dst + " checkout " + last_exploitdb_commit, shell=True)

    with open(exploits_path, 'r', encoding="utf8") as fin:
        dr = csv.DictReader(fin)
        exploit_dates_list = [(i['id'], i['date']) for i in dr]
    

    with open(shellcodes_path, 'r', encoding="utf8") as fin:
        dr = csv.DictReader(fin)
        shellcode_dates_list = [(i['id'], i['date']) for i in dr]

    session = start_session()
    for exploit_date in exploit_dates_list:
        try:
            edited_exploit = session.query(Exploit).get(exploit_date[0])
            edited_exploit.date = str(exploit_date[1])
            session.commit()
        except AttributeError:
            # print("ERROR:", exploit_date[0], exploit_date[1])
            pass

    for shellcode_date in shellcode_dates_list:
        try:
            edited_shellcode = session.query(Shellcode).get(shellcode_date[0])
            edited_shellcode.date = str(shellcode_date[1])
            session.commit()
        except AttributeError:
            print("ERROR:", shellcode_date[0], shellcode_date[1])

    session.close()
