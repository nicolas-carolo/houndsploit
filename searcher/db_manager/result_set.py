from sqlalchemy import or_
from searcher.db_manager.models import Exploit, Shellcode
from searcher.db_manager.session_manager import start_session


def queryset2list(queryset):
    """
    Convert a queryset into a list
    :param queryset: the queryset to be converted.
    :return: the list corresponding to the queryset.
    """
    list = []
    for instance in queryset:
        list.append(instance)
    return list


def void_result_set():
    """
    Create a void result set.
    :return: a void list.
    """
    list = []
    return list


def result_set_len(result_set):
    """
    Calculate the length of a result set.
    :param result_set: the result set we want to know the length.
    :return: the length of the result set.
    """
    try:
        return len(result_set)
    except TypeError:
        return 0


def join_result_sets(result_set_1, result_set_2, db_table):
    """
    Make the union of two result sets, excluding the duplicates.
    :param result_set_1: the first result set.
    :param result_set_2: the second result set.
    :param db_table: the database table.
    :return: the result set obtained by the union of the two result sets.
    """
    list_id_1 = []
    list_id_2 = []
    for instance in result_set_1:
        list_id_1.append(instance.id)
    for instance in result_set_2:
        list_id_2.append(instance.id)
    union_list_id = set(list_id_1) | set(list_id_2)

    if len(union_list_id) == 0:
        return void_result_set()

    session = start_session()
    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(or_(Exploit.id == instance_id for instance_id in union_list_id))
    else:
        queryset = session.query(Shellcode).filter(or_(Shellcode.id == instance_id for instance_id in union_list_id))

    session.close()
    return queryset2list(queryset)
