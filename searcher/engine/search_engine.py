import re

from searcher.engine.string import str_is_num_version
from searcher.engine.filter_query import filter_exploits_without_comparator, filter_exploits_with_comparator,\
    filter_shellcodes_without_comparator, filter_shellcodes_with_comparator

from sqlalchemy import and_, or_
from searcher.db_manager.models import Exploit, Shellcode
from searcher.db_manager.session_manager import start_session
from searcher.db_manager.result_set import queryset2list, void_result_set, join_result_sets

N_MAX_RESULTS_NUMB_VERSION = 20000


def search_vulnerabilities_in_db(searched_text, db_table):
    """
    Perform a search in the database.
    :param searched_text: the text searched by the user.
    :param db_table: the database table in which perform the search.
    :return: the list containing the result of the performed search.
    """
    word_list = str(searched_text).split()
    if str(searched_text).isnumeric():
        return search_vulnerabilities_numerical(word_list[0], db_table)
    elif str_is_num_version(str(searched_text)) and str(searched_text).__contains__(' ') and not str(
            searched_text).__contains__('<'):
        result_set = search_vulnerabilities_version(word_list, db_table)
        # union with standard research
        std_result_set = search_vulnerabilities_for_text_input(searched_text, db_table)
        union_result_set = join_result_sets(result_set, std_result_set, db_table)
        if len(union_result_set) > 0:
            return union_result_set
        else:
            return search_vulnerabilities_for_description(word_list, db_table)
    else:
        result_set = search_vulnerabilities_for_description(word_list, db_table)
        if len(result_set) > 0:
            return result_set
        else:
            result_set = search_vulnerabilities_for_file(word_list, db_table)
            if len(result_set) > 0:
                return result_set
            else:
                return search_vulnerabilities_for_author(word_list, db_table)


def search_vulnerabilities_numerical(searched_text, db_table):
    """
    Perform a search based on vulnerabilities' description, file, id, and port (only if it is an exploit) for an only
    numerical search input.
    :param searched_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset with search results.
    """
    session = start_session()
    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(or_(Exploit.description.like('%' + searched_text + '%'),
                                                     Exploit.id == int(searched_text),
                                                     Exploit.file.like('%' + searched_text + '%'),
                                                     Exploit.port == int(searched_text)
                                                     ))
    else:
        queryset = session.query(Shellcode).filter(or_(Shellcode.description.like('%' + searched_text + '%'),
                                                       Shellcode.id == int(searched_text),
                                                       Shellcode.file.like('%' + searched_text + '%')
                                                       ))
    session.close()
    return queryset2list(queryset)


def search_vulnerabilities_for_description(word_list, db_table):
    """
    Search vulnerabilities for description.
    :param word_list: the list of words searched by the user.
    :param db_table: the database table in which perform the search.
    :return: the list containing the results of the performed search.
    """
    session = start_session()

    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(and_(Exploit.description.like('%' + word + '%') for word in word_list))
    else:
        queryset = session.query(Shellcode).filter(
            and_(Shellcode.description.like('%' + word + '%') for word in word_list))

    session.close()
    return queryset2list(queryset)


def search_vulnerabilities_for_file(word_list, db_table):
    """
    Search vulnerabilities for file.
    :param word_list: the list of words searched by the user.
    :param db_table: the database table in which perform the search.
    :return: the list containing the results of the performed search.
    """
    session = start_session()

    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(and_(Exploit.file.like('%' + word + '%') for word in word_list))
    else:
        queryset = session.query(Shellcode).filter(
            and_(Shellcode.file.like('%' + word + '%') for word in word_list))

    session.close()
    return queryset2list(queryset)


def search_vulnerabilities_for_author(word_list, db_table):
    """
    Search vulnerabilities for author.
    :param word_list: the list of words searched by the user.
    :param db_table: the database table in which perform the search.
    :return: the list containing the results of the performed search.
    """
    session = start_session()

    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(and_(Exploit.author.like('%' + word + '%') for word in word_list))
    else:
        queryset = session.query(Shellcode).filter(
            and_(Shellcode.author.like('%' + word + '%') for word in word_list))

    session.close()
    return queryset2list(queryset)


def search_vulnerabilities_version(word_list, db_table):
    """
    Search vulnerabilities for version number.
    :param word_list: the list of words searched by the user.
    :param db_table: the database table in which perform the search.
    :return: the list containing the results of the performed search.
    """
    software_name = word_list[0]
    for word in word_list[1:]:
        if not str_is_num_version(word):
            software_name = software_name + ' ' + word
        else:
            num_version = word
    if db_table == 'searcher_exploit':
        return search_exploits_version(software_name, num_version)
    else:
        return search_shellcodes_version(software_name, num_version)


def search_exploits_version(software_name, num_version):
    """
    Perform a search based on exploits' description for an input search that contains a number of version.
    This function is called by 'search_vulnerabilities_version' method.
    :param software_name: the name of the software that the user is searching for.
    :param num_version: the specific number of version the user is searching for.
    :return: a queryset with search result found in 'searcher_exploit' DB table.
    """
    session = start_session()
    queryset = session.query(Exploit).filter(and_(Exploit.description.like('%' + software_name + '%')))
    query_result_set = queryset2list(queryset)
    session.close()
    # limit the time spent for searching useless results.
    if queryset.count() > N_MAX_RESULTS_NUMB_VERSION:
        return void_result_set()
    final_result_set = []
    for exploit in query_result_set:
        # if exploit not contains '<'
        if not str(exploit.description).__contains__('<'):
            final_result_set = filter_exploits_without_comparator(exploit, num_version, software_name, final_result_set)
        # if exploit contains '<'
        else:
            final_result_set = filter_exploits_with_comparator(exploit, num_version, software_name, final_result_set)
    return final_result_set


def search_shellcodes_version(software_name, num_version):
    """
    Perform a search based on exploits' description for an input search that contains a number of version.
    This function is called by 'search_vulnerabilities_version' method.
    :param software_name: the name of the software that the user is searching for.
    :param num_version: the specific number of version the user is searching for.
    :return: a queryset with search result found in 'searcher_exploit' DB table.
    """
    session = start_session()
    queryset = session.query(Shellcode).filter(and_(Shellcode.description.like('%' + software_name + '%')))
    query_result_set = queryset2list(queryset)
    session.close()
    # limit the time spent for searching useless results.
    if queryset.count() > N_MAX_RESULTS_NUMB_VERSION:
        # return Exploit.objects.none()
        return void_result_set()
    final_result_set = []
    for shellcode in query_result_set:
        # if exploit not contains '<'
        if not str(shellcode.description).__contains__('<'):
            final_result_set = filter_shellcodes_without_comparator(shellcode, num_version, software_name, final_result_set)
        # if exploit contains '<'
        else:
            final_result_set = filter_shellcodes_with_comparator(shellcode, num_version, software_name, final_result_set)
    return final_result_set


def search_vulnerabilities_for_text_input(searched_text, db_table):
    """
    Perform a search in description based on characters contained by this attribute.
    This queryset can be joined with the search results based on the number of version.
    :param search_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset containing the search results found with a search based on the characters contained by
                the attribute 'description'
    """
    word_list = str(searched_text).split()
    word_list_num = []
    for word in word_list:
        if word.isnumeric():
            word_list.remove(word)
            word_list_num.append(' ' + word)
            word_list_num.append('/' + word)
        if word.__contains__('.'):
            word_list.remove(word)
            word_list_num.append(' ' + word)
            word_list_num.append('/' + word)
    try:
        session = start_session()
        if db_table == 'searcher_exploit':
            queryset = session.query(Exploit).filter(
                and_(Exploit.description.like('%' + word + '%') for word in word_list))
        else:
            queryset = session.query(Shellcode).filter(
                and_(Shellcode.description.like('%' + word + '%') for word in word_list))
        session.close()
        query_result_set = queryset2list(queryset)
    except TypeError:
        query_result_set = void_result_set()
    final_result_set = []
    try:
        for instance in query_result_set:
            for word in word_list_num:
                if str(instance.description).__contains__(word) and not list(final_result_set).__contains__(instance):
                    final_result_set.append(instance)
    except TypeError:
        pass
    return final_result_set


def get_exploit_by_id(exploit_id):
    session = start_session()
    exploit = session.query(Exploit).get(exploit_id)
    session.close()
    return exploit


def get_shellcode_by_id(shellcode_id):
    session = start_session()
    shellcode = session.query(Shellcode).get(shellcode_id)
    session.close()
    return shellcode


def get_vulnerability_extension(vulnerability_file):
    """
    Get the extension of the vulnerability passed as parameter.
    :param vulnerability_file: the vulnerability we want to get its extension.
    :return: the extension of the vulnerability passed as parameter.
    """
    regex = re.search(r'\.(?P<extension>\w+)', vulnerability_file)
    extension = '.' + regex.group('extension')
    return extension

