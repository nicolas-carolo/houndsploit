from flask import request


def get_searched_text(request):
    searched_text = request.args.get('searched-text', None)
    return searched_text


def is_previous_page_bookmarks(request):
    is_prev_page_bookmarks = request.args.get('isprevpagebookmarks', None)
    if is_prev_page_bookmarks == "true":
        return True
    else:
        return False
