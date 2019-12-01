# -*- encoding: utf-8 -*-
# houndsploit v2.0.0
# An advanced graphic search engine for Exploit-DB
# Copyright © 2019, Nicolas Carolo.
# See /LICENSE for licensing information.

"""
INSERT MODULE DESCRIPTION HERE.

:Copyright: © 2019, Nicolas Carolo.
:License: BSD (see /LICENSE).
"""

__all__ = ()

import sys
import os
from HoundSploit.cl_parser import parse_args
from HoundSploit.app import start_app
from HoundSploit.searcher.engine.updates import install_exploitdb_update



def main():
    """Main routine of houndsploit."""
    init_path = os.path.split(sys.executable)[0]
    if not os.path.isfile(init_path + "/HoundSploit/hound_db.sqlite3"):
        install_exploitdb_update()
    start_app()
