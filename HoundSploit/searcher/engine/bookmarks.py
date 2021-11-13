from HoundSploit.searcher.db_manager.models import Bookmark, Exploit, Shellcode
from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.db_manager.result_set import queryset2list
from HoundSploit.searcher.engine.utils import check_file_existence, check_vulnerability_existence
from datetime import datetime
import os


init_path = exploitdb_path = os.path.expanduser("~") + "/.HoundSploit"


def new_bookmark(vulnerability_id, vulnerability_class):
    """
    Create a new bookmark.
    :param vulnerability_id: the id of the vulnerability.
    :param vulnerability_class: the class of the vulnerability (exploit or shellcode).
    :return: True if the exploit was correctly created, otherwise False.
    """
    if not is_bookmarked(vulnerability_id, vulnerability_class) and check_vulnerability_existence(vulnerability_id, vulnerability_class):
        session = start_session()
        today = datetime.now()
        new_bookmark = Bookmark(vulnerability_id, vulnerability_class, today)
        session.add(new_bookmark)
        add_bookmark_to_custom_csv(vulnerability_id, vulnerability_class, today)
        session.commit()
        session.close()
        return True
    else:
        return False


def add_bookmark_to_custom_csv(vulnerability_id, vulnerability_class, date):
    """
    Add the bookmark record to the CSV file used to restore the database when
    HoundSploit is updated to a new version.
    :param vulnerability_id: the id of the vulnerability.
    :param vulnerability_class: the class of the vulnerability (exploit or shellcode).
    :param date: the date when the bookmark was created.
    """
    bookmarks_file = init_path + "/bookmarks.csv"
    if not check_file_existence(bookmarks_file):
        f= open(bookmarks_file, "w+")
        f.write("vulnerability_id,vulnerability_class,date\n")
        f.close()
    f= open(bookmarks_file, "a+")
    f.write(vulnerability_id + "," + vulnerability_class + ",\"" + str(date) + "\"\n")
    f.close()


def remove_bookmark(vulnerability_id, vulnerability_class):
    """
    Delete the bookmark uniquely identified by the vulnerability's id.
    :param vulnerability_id: the id of the vulnerability to be deleted.
    :param vulnerability_class: the class of the vulnerability (exploit or shellcode).
    :return: True if the vulnerability was correctly deleted, otherwise False.
    """
    if is_bookmarked(vulnerability_id, vulnerability_class):
        session = start_session()
        session.query(Bookmark).filter(Bookmark.vulnerability_id == vulnerability_id,
                                    Bookmark.vulnerability_class == vulnerability_class).delete()
        session.commit()
        session.close()
        delete_bookmark_from_csv(vulnerability_id, vulnerability_class)
        return True
    else:
        return False


def delete_bookmark_from_csv(vulnerability_id, vulnerability_class):
    """
    Delete the bookmark record from the CSV file used to restore the database when
    HoundSploit is updated to a new version.
    :param vulnerability_id: the id of the vulnerability to be removed.
    :param vulnerability_class: the class of the vulnerability (exploit or shellcode).
    """
    bookmarks_file = init_path + "/bookmarks.csv"
    with open(bookmarks_file, "r") as f:
        lines = f.readlines()
    f= open(bookmarks_file, "w+")
    f.write("vulnerability_id,vulnerability_class,date\n")
    f.close()
    with open(bookmarks_file, "a+") as f:
        for line in lines[1:]:
            if not line.startswith(vulnerability_id + "," + vulnerability_class):
                f.write(line)


def is_bookmarked(vulnerability_id, vulnerability_class):
    """
    Check if a vulnerability is already bookmarked.
    :param vulnerability_id: the id of the vulnerability.
    :param vulnerability_class: the class of the vulnerability (exploit or shellcode).
    :return: True if the vulnerability is already bookmarked, otherwise False.
    """
    session = start_session()
    queryset = session.query(Bookmark).filter(Bookmark.vulnerability_id == vulnerability_id,
                                        Bookmark.vulnerability_class == vulnerability_class)
    results_list = queryset2list(queryset)
    session.close()
    if len(results_list) == 0:
        return False
    else:
        return True


def get_bookmarks_list():
    """
    Get the list of bookmarks.
    :return: a list containing the bookmarks.
    """
    bookmarks_list = []
    session = start_session()
    queryset = session.query(Bookmark)
    result_list = queryset2list(queryset)
    for bookmark in result_list:
        if bookmark.vulnerability_class == 'exploit':
            print(bookmark.vulnerability_id)
            queryset = session.query(Exploit).filter(Exploit.id == bookmark.vulnerability_id)
        else:
            queryset = session.query(Shellcode).filter(Shellcode.id == bookmark.vulnerability_id)
        try:
            bookmark_item = queryset2list(queryset)[0]
            bookmarks_list.append(bookmark_item)
        except IndexError:
            pass
    return bookmarks_list