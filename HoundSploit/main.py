# -*- encoding: utf-8 -*-
# houndsploit v2.7.0
# An advanced graphic search engine for Exploit-DB
# Copyright © 2021, Nicolas Carolo.
# See /LICENSE for licensing information.

"""
INSERT MODULE DESCRIPTION HERE.

:Copyright: © 2021, Nicolas Carolo.
:License: BSD (see /LICENSE).
"""

__all__ = ()

from HoundSploit.cl_parser import parse_args
from HoundSploit.app import start_app
from HoundSploit.searcher.engine.csv2sqlite import create_db
from HoundSploit.searcher.engine.fix_dates import create_fixed_db
from HoundSploit.searcher.utils.file import check_file_existence
from HoundSploit.searcher.engine.updates import migrate_to_new_installation
import os
import platform
from os import path



def main():
    """Main routine of houndsploit."""
    if platform.system() == "Windows":
        init_path = os.path.expanduser("~") + "\.HoundSploit"
        if check_file_existence(init_path + "/houndsploit_sw.lock"):
            print("Before executing HoundSploit run:")
            print("\tPS> pip install -r " + init_path + "\houndsploit\requirements.txt")
            print("\tPS> cd " + init_path + "\houndsploit")
            print("\tPS> python setup.py install")
            print("\tPS> rm " + init_path + "\houndsploit_sw.lock")
            print("\tPS> houndsploit")
            exit(1)
        if check_file_existence(init_path + "/.delete_db.lock"):
            os.remove(os.path.abspath(init_path + "/hound_db.sqlite3"))
            os.remove(os.path.abspath(init_path + "/.delete_db.lock"))
        if not os.path.isfile(init_path + "\hound_db.sqlite3") and not os.path.isdir(init_path + "\\fixed_exploitdb"):
            create_db()
        elif not os.path.isfile(init_path + "\hound_db.sqlite3") and os.path.isdir(init_path + "\\fixed_exploitdb"):
            create_fixed_db()
    else:
        init_path = os.path.expanduser("~") + "/.HoundSploit"
        if not path.exists(init_path):
            migrate_to_new_installation()
        if check_file_existence(init_path + "/houndsploit_sw.lock"):
            print("Before executing HoundSploit run:")
            print("\t$ pip install -r " + init_path + "/houndsploit/requirements.txt")
            print("\t$ cd " + init_path + "/houndsploit")
            print("\t$ python setup.py install")
            print("\t$ rm " + init_path + "/houndsploit_sw.lock")
            print("\t$ houndsploit")
            exit(1)
        if not os.path.isfile(init_path + "/hound_db.sqlite3") and not os.path.isdir(init_path + "/fixed_exploitdb"):
            create_db()
        elif not os.path.isfile(init_path + "/hound_db.sqlite3") and os.path.isdir(init_path + "/fixed_exploitdb"):
            create_fixed_db()
    start_app()




