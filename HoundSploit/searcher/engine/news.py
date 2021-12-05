import datetime
from HoundSploit.searcher.db_manager.models import Exploit, Shellcode
from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.db_manager.result_set import queryset2list
from HoundSploit.searcher.engine.filter_query import filter_vulnerabilities_for_date_range


def get_latest_exploits_list():
    """
    Get the list of the latest exploits.
    :return: a list containing the latest exploits.
    """
    session = start_session()
    last_db_update_date = datetime.datetime.strptime('2021-12-01', '%Y-%m-%d')
    today_date = datetime.datetime.strptime('2021-12-05', '%Y-%m-%d')
    queryset = session.query(Exploit)
    exploits_list = queryset2list(queryset)
    exploits_list = filter_vulnerabilities_for_date_range(exploits_list, last_db_update_date, today_date)
    session.close()
    return exploits_list