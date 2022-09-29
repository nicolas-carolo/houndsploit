from HoundSploit.searcher.entities.bookmark import Bookmark
from HoundSploit.searcher.entities.exploit import Exploit
from HoundSploit.searcher.entities.shellcode import Shellcode
from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.db_manager.result_set import queryset2list
from HoundSploit.searcher.utils.csv import add_bookmark_to_csv, delete_bookmark_from_csv
from HoundSploit.searcher.utils.file import check_file_existence
from datetime import datetime


def new_bookmark(vulnerability_id, vulnerability_class):
    if can_be_bookmarked(vulnerability_id, vulnerability_class):
        session = start_session()
        today = datetime.now()
        new_bookmark = Bookmark(vulnerability_id, vulnerability_class, today)
        session.add(new_bookmark)
        add_bookmark_to_csv(vulnerability_id, vulnerability_class, today)
        session.commit()
        session.close()
        return True
    else:
        return False


def can_be_bookmarked(vulnerability_id, vulnerability_class):
    if vulnerability_class == 'exploit':
        vulnerability_obj = Exploit.get_by_id(vulnerability_id)
    elif vulnerability_class == 'shellcode':
        vulnerability_obj = Shellcode.get_by_id(vulnerability_id)
    if vulnerability_obj is not None:
        if not is_bookmarked(vulnerability_id, vulnerability_class):
            return True
        else:
            return False
    else:
        return False


def remove_bookmark(vulnerability_id, vulnerability_class):
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


def is_bookmarked(vulnerability_id, vulnerability_class):
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
    bookmarks_list = []
    session = start_session()
    queryset = session.query(Bookmark)
    result_list = queryset2list(queryset)
    session.close()
    for bookmark in result_list:
        if bookmark.vulnerability_class == 'exploit':
            bookmark_item = Exploit.get_by_id(bookmark.vulnerability_id)
        else:
            bookmark_item = Shellcode.get_by_id(bookmark.vulnerability_id)
        if bookmark_item is not None:
            bookmarks_list.append(bookmark_item)
    return bookmarks_list