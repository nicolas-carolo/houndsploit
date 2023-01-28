from HoundSploit.searcher.entities.bookmark import Bookmark
from HoundSploit.searcher.entities.exploit import Exploit
from HoundSploit.searcher.entities.shellcode import Shellcode
from HoundSploit.searcher.db_manager.session_manager import start_session
from HoundSploit.searcher.db_manager.result_set import queryset2list
from HoundSploit.searcher.utils.csv import add_bookmark_to_csv, delete_bookmark_from_csv
from HoundSploit.searcher.utils.file import check_file_existence
from HoundSploit.searcher.utils.constants import N_RESULTS_FOR_PAGE
from datetime import datetime


def new_bookmark(vulnerability):
    if vulnerability is None:
        return False, 'Sorry! This item does not exist :('
    if vulnerability.type == 'shellcode':
        vulnerability_class = 'shellcode'
    else:
        vulnerability_class = 'exploit'
    if can_be_bookmarked(vulnerability, vulnerability_class):
        session = start_session()
        today = datetime.now()
        new_bookmark = Bookmark(vulnerability.id, vulnerability_class, today)
        session.add(new_bookmark)
        add_bookmark_to_csv(vulnerability.id, vulnerability_class, today)
        session.commit()
        session.close()
        return True, "New bookmark added"
    else:
        return False, 'Sorry! This item cannot be bookmarked :('


def can_be_bookmarked(vulnerability, vulnerability_class):
    if vulnerability is not None:
        if not is_bookmarked(vulnerability.id, vulnerability_class):
            return True
        else:
            return False
    else:
        return False


def remove_bookmark(vulnerability):
    if vulnerability is None:
        return False, 'Sorry! This item does not exist :('
    if vulnerability.type == 'shellcode':
        vulnerability_class = 'shellcode'
    else:
        vulnerability_class = 'exploit'
    if is_bookmarked(vulnerability.id, vulnerability_class):
        session = start_session()
        session.query(Bookmark).filter(Bookmark.vulnerability_id == vulnerability.id,
                                    Bookmark.vulnerability_class == vulnerability_class).delete()
        session.commit()
        session.close()
        delete_bookmark_from_csv(vulnerability.id, vulnerability_class)
        return True, "Bookmark deleted"
    else:
        return False, 'Sorry! This bookmark cannot be deleted :('


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


def get_filtered_bookmarks_list(searched_text):
    bookmarks_list = get_bookmarks_list()
    exploits_list = Exploit.search(searched_text)
    shellcodes_list = Shellcode.search(searched_text)
    results_list = exploits_list + shellcodes_list
    filtered_bookmarks_list = []
    for result in results_list:
        for bookmark in bookmarks_list:
            if result.description == bookmark.description:
                filtered_bookmarks_list.append(bookmark)
    return filtered_bookmarks_list
