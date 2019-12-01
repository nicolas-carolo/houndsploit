from sqlalchemy import or_
from HoundSploit.searcher.db_manager.models import Exploit, Shellcode
from HoundSploit.searcher.db_manager.session_manager import start_session


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

