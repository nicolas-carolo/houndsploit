from HoundSploit.searcher.utils.constants import N_RESULTS_FOR_PAGE
from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.entities.exploit import Exploit
from HoundSploit.searcher.entities.shellcode import Shellcode
from HoundSploit.searcher.db_manager.result_set import queryset2filterlist
from HoundSploit.searcher.utils.list import remove_list_duplicates

def get_n_needed_pages_for_showing_results(n_results):
    if n_results % N_RESULTS_FOR_PAGE == 0:
        return int(n_results / N_RESULTS_FOR_PAGE)
    else:
        return int(n_results / N_RESULTS_FOR_PAGE) + 1


def get_vulnerability_filters():
    types_list = get_vulnerability_types()
    platforms_list = get_vulnerability_platforms()
    return types_list, platforms_list


def get_vulnerability_types():
    session = start_session()
    queryset = session.query(Exploit.type).distinct()
    exploit_types_list = queryset2filterlist(queryset)
    queryset = session.query(Shellcode.type).distinct()
    shellcode_types_list = queryset2filterlist(queryset)
    session.close()
    types_list = remove_list_duplicates(exploit_types_list + shellcode_types_list)
    types_list = sorted(types_list)
    return types_list


def get_vulnerability_platforms():
    session = start_session()
    queryset = session.query(Exploit.platform).distinct()
    exploit_platforms_list = queryset2filterlist(queryset)
    queryset = session.query(Shellcode.platform).distinct()
    shellcode_platforms_list = queryset2filterlist(queryset)
    session.close()
    platforms_list = remove_list_duplicates(exploit_platforms_list + shellcode_platforms_list)
    platforms_list = sorted(platforms_list)
    return platforms_list


def get_index_first_result(current_bookmarks_page):
    return (int(current_bookmarks_page) - 1) * N_RESULTS_FOR_PAGE


def get_index_last_result(index_first_result):
    return index_first_result + N_RESULTS_FOR_PAGE