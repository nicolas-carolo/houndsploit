from HoundSploit.searcher.db_manager.models import Exploit, Shellcode
from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.db_manager.result_set import queryset2list


def get_latest_exploits_list():
    """
    Get the list of the latest exploits.
    :return: a list containing the latest exploits.
    """
    session = start_session()
    queryset = session.query(Exploit).filter(Exploit.date == '2021-11-18')
    exploits_list = queryset2list(queryset)
    session.close()
    return exploits_list