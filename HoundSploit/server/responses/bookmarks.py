from flask import render_template
from HoundSploit.searcher.engine.bookmarks import get_bookmarks_list, get_filtered_bookmarks_list, get_index_first_bookmark_result,\
    get_index_last_bookmark_result
from HoundSploit.searcher.utils.searcher import get_n_needed_pages_for_showing_results
from HoundSploit.searcher.engine.keywords_highlighter import highlight_keywords_in_description



def render_bookmarks(searched_text, current_bookmarks_page):
    key_words_list = []
    if searched_text == "":
        bookmarks_list = get_bookmarks_list()
    else:
        key_words_list = (str(searched_text).upper()).split()
        bookmarks_list = get_filtered_bookmarks_list(searched_text)
    n_bookmarks = len(bookmarks_list)
    latest_bookmarks_page = get_n_needed_pages_for_showing_results(n_bookmarks)
    if current_bookmarks_page > latest_bookmarks_page:
        current_bookmarks_page = latest_bookmarks_page
    index_first_result = get_index_first_bookmark_result(current_bookmarks_page)
    index_last_result = get_index_last_bookmark_result(index_first_result)
    bookmarks_list = bookmarks_list[index_first_result:index_last_result]
    bookmarks_list = highlight_keywords_in_description(key_words_list, bookmarks_list)
    return render_template('bookmarks.html', searched_text=searched_text,
                            bookmarks_list=bookmarks_list,
                            current_bookmarks_page=current_bookmarks_page,
                            latest_bookmarks_page=latest_bookmarks_page)