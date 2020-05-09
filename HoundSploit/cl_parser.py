# -*- encoding: utf-8 -*-
# houndsploit v2.2.1
# An advanced graphic search engine for Exploit-DB
# Copyright © 2019, Nicolas Carolo.
# See /LICENSE for licensing information.

"""
Command Line Parsing Module for houndsploit

:Copyright: © 2019, Nicolas Carolo.
:License: BSD (see /LICENSE).
"""

__all__ = ()

import argparse




def parse_args(args):
    """
    This function parses the arguments which have been passed from the command
    line, these can be easily retrieved for example by using "sys.argv[1:]".
    It returns a parser object as with argparse.

    Arguments:
    args -- the list of arguments passed from the command line as the sys.argv
            format

    Returns: a parser with the provided arguments, which can be used in a
            simpler format
    """
    parser = argparse.ArgumentParser(prog='houndsploit',
                                     description='An advanced graphic search engine for Exploit-DB')

    parser.add_argument(
        "url",
        help="the URL to fuzz",
        type=str,
        )
    parser.add_argument(
        "-w", "--wordlist",
        action='append',
        help="input wordlist used for fuzzing",
        default=[],
        type=str,
        nargs='+',
        )
    parser.add_argument(
        "-s", "--concurrency",
        help="number of concurrent http requests",
        default=20,
        type=int,
        )
    parser.add_argument(
        "-d", "--data",
        help="data passed in the body, when set, the request will be a POSt",
        action='append',
        default=[],
        type=str,
        nargs='+',
        )
    parser.add_argument(
        "-H", "--header",
        help="A header that will be passed within the requests",
        action='append',
        default=[],
        type=str,
        nargs='+',
        )


    return parser.parse_args(args)
