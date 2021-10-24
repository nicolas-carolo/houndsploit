import subprocess
import os
import platform
import csv
import re
from distutils.dir_util import copy_tree
from HoundSploit.searcher.db_manager.models import Exploit, Shellcode
from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.db_manager.result_set import queryset2list

last_exploitdb_commit = "23acd8a13b7a871e735016897c7a9e7b0ac33448"
exploitdb_url = "https://www.exploit-db.com/exploits/"
date_pattern = "<meta property=\"article:published_time\" content=\"(.*?)\" />"


shellcode_dates_dict = {
    '50291': "2021-09-13",
    '50368': "2021-10-01"
}


def fix_dates():
    fix_known_dates()
    fix_unknown_dates()


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

    # TODO download old commit only if the folder does not exists
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
            print("FIXED: Exploit", exploit_date[0], exploit_date[1])
        except AttributeError:
            print("ERROR: Exploit", exploit_date[0], exploit_date[1])
            pass

    for shellcode_date in shellcode_dates_list:
        try:
            edited_shellcode = session.query(Shellcode).get(shellcode_date[0])
            edited_shellcode.date = str(shellcode_date[1])
            session.commit()
            print("FIXED: Shellcode", shellcode_date[0], shellcode_date[1])
        except AttributeError:
            print("ERROR: Shellcode", shellcode_date[0], shellcode_date[1])

    session.close()


def fix_unknown_dates():
    session = start_session()

    queryset = session.query(Exploit).filter(Exploit.date == '1970-01-01')
    exploits_list = queryset2list(queryset)
    for exploit in exploits_list:
        exploit_url = exploitdb_url + exploit.id
        print(exploit_url)

        try:
            bash_command = "curl " + exploit_url
            # print(bash_command)
            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            # print(output)

            page_source = output.decode("utf-8")
            exploit_date = re.search(date_pattern, page_source).group(1)
            edited_exploit = session.query(Exploit).get(exploit.id)
            edited_exploit.date = str(exploit_date)
            session.commit()
            print("FIXED: Exploit", exploit.id, exploit.date)
        except AttributeError:
            print("ERROR: Exploit", exploit.id)

    queryset = session.query(Shellcode).filter(Shellcode.date == '1970-01-01')
    shellcodes_list = queryset2list(queryset)
    for shellcode in shellcodes_list:
        try:
            edited_shellcode = session.query(Shellcode).get(shellcode.id)
            edited_shellcode.date = shellcode_dates_dict[shellcode.id]
            session.commit()
            print("FIXED: Shellcode", shellcode.id, shellcode.date)
        except AttributeError:
            print("ERROR: Shellcode", shellcode.id)
    session.close()


def create_fixed_db():
    if platform.system() == "Windows":
        houndsploit_path = os.path.expanduser("~") + "\.HoundSploit\\"
        exploitdb_path = os.path.expanduser("~") + "\.HoundSploit\\exploitdb\\"
    else:
        houndsploit_path = os.path.expanduser("~") + "/.HoundSploit/"
        exploitdb_path = os.path.expanduser("~") + "/.HoundSploit/exploitdb/"
    subprocess.check_output("cp " + houndsploit_path + "fixed_hound_db.sqlite3 " + houndsploit_path + "hound_db.sqlite3", shell=True)
    add_new_exploits_to_db(exploitdb_path, houndsploit_path)


def add_new_exploits_to_db(exploitdb_path, houndsploit_path):
    """
    bash_command_1 = "diff " + exploitdb_path + "files_exploits.csv " + houndsploit_path + "old_files_exploits.csv"
    bash_command_2 = "grep '[<>]'"
    p1 = subprocess.Popen(bash_command_1.split(), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(bash_command_2.split(), stdin=p1.stdout, stdout=subprocess.PIPE)
    output, error = p2.communicate()
    exploit_diff = output.decode("utf-8")
    """
    with open(houndsploit_path + "old_files_exploits.csv", 'r') as t1, open(exploitdb_path + "files_exploits.csv", 'r') as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()

    for line in filetwo:
        if line not in fileone:
            print(line)

    # print(exploit_diff)
    # TODO complete function
