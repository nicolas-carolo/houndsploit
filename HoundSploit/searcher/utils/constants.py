import os

BASE_DIR = os.path.expanduser("~") + "/.HoundSploit/"
EXPLOITDB_PATH = os.path.abspath(BASE_DIR + "exploitdb")
#TEMPLATE_DIR = os.path.abspath(BASE_DIR + 'houndsploit/HoundSploit/templates')
#STATIC_DIR = os.path.abspath(BASE_DIR + 'houndsploit/HoundSploit/static')
TEMPLATE_DIR = os.path.abspath('/home/nicolas/Projects/Python/houndsploit/HoundSploit/templates')
STATIC_DIR = os.path.abspath('/home/nicolas/Projects/Python/houndsploit/HoundSploit/static')

N_RESULTS_FOR_PAGE = 10
DEFAULT_SUGGESTIONS = ["joomla", "linux", "phpbb", "macos", "mac os x", "html 5", "wordpress"]