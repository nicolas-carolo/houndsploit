import re
from HoundSploit.searcher.db_manager.models import Bookmark
from HoundSploit.searcher.entities.exploit import Exploit
from HoundSploit.searcher.entities.shellcode import Shellcode
from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.db_manager.result_set import queryset2list


N_RESULTS_FOR_PAGE = 10


def check_file_existence(filename):
    try:
        f = open(filename)
        f.close()
        return True
    except IOError:
        return False


def get_vulnerability_extension(vulnerability_file):
    """
    Get the extension of the vulnerability passed as parameter.
    :param vulnerability_file: the vulnerability we want to get its extension.
    :return: the extension of the vulnerability passed as parameter.
    """
    regex = re.search(r'\.(?P<extension>\w+)', vulnerability_file)
    extension = '.' + regex.group('extension')
    return extension   


def get_n_needed_pages(n_results):
    """
    Get the number of pages needed for show search results.
    :param n_results: the number of results to show.
    :return: the number of pages needed.
    """
    if n_results % N_RESULTS_FOR_PAGE == 0:
        return int(n_results / N_RESULTS_FOR_PAGE)
    else:
        return int(n_results / N_RESULTS_FOR_PAGE) + 1


def check_vulnerability_existence(vulnerability_id, vulnerability_class):
    session = start_session()
    if vulnerability_class == "exploit":
        queryset = session.query(Exploit).filter(Exploit.id == vulnerability_id)
    else:
        queryset = session.query(Shellcode).filter(Shellcode.id == vulnerability_id)
    results_list = queryset2list(queryset)
    if len(results_list) == 0:
        session.close()
        return False
    else:
        session.close()
        return True

