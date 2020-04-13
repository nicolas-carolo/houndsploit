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

from HoundSploit.cl_parser import parse_args
from HoundSploit.app import start_app
from HoundSploit.searcher.engine.csv2sqlite import create_db
import os



def main():
    """Main routine of houndsploit."""
    init_path = os.path.expanduser("~") + "/HoundSploit"
    if not os.path.isfile(init_path + "/hound_db.sqlite3"):
        create_db()
    start_app()
