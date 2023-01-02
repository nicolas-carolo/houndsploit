import os

BASE_DIR = os.path.expanduser("~") + "/.HoundSploit/"
EXPLOITDB_PATH = os.path.abspath(BASE_DIR + "exploitdb")
TEMPLATE_DIR = os.path.abspath(BASE_DIR + 'houndsploit/HoundSploit/templates')
STATIC_DIR = os.path.abspath(BASE_DIR + 'houndsploit/HoundSploit/static')

N_RESULTS_FOR_PAGE = 10