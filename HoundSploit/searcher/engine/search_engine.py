from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.entities.exploit import Exploit
from HoundSploit.searcher.entities.shellcode import Shellcode
from HoundSploit.searcher.db_manager.result_set import queryset2list
from HoundSploit.searcher.engine.lists import remove_list_duplicates

def get_vulnerability_filters():
    """
    Get the list of all vulnerability filters
    :return: a list containing all vulnerability types and a list containing all platforms
    """
    session = start_session()
    queryset = session.query(Exploit)
    exploits_list = queryset2list(queryset)
    types_list = []
    platform_list = []
    for exploit in exploits_list:
        types_list.append(exploit.type)
        platform_list.append(exploit.platform)
    queryset = session.query(Shellcode)
    shellcodes_list = queryset2list(queryset)
    for shellcode in shellcodes_list:
        types_list.append(shellcode.type)
        platform_list.append(shellcode.platform)
    types_list = sorted(remove_list_duplicates(types_list))
    platform_list = sorted(remove_list_duplicates(platform_list))
    session.close()
    return types_list, platform_list