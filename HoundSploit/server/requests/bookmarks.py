from flask import request


def get_bookmarks_request_params(request):
    searched_text = get_searched_text(request)
    current_bookmarks_page = get_current_bookmarks_page(request)
    return searched_text, current_bookmarks_page


def get_searched_text(request):
    if request.method == 'POST':
        searched_text = request.form['searched-text']
    else:
        searched_text = request.args.get('searched', None)
    if searched_text is None:
        searched_text = ""
    return searched_text


def get_current_bookmarks_page(request):
    if request.method == 'POST':
        current_bookmarks_page = int(request.form['hid-b-page'])
        if current_bookmarks_page < 1:
            current_bookmarks_page = 1
    else:
        current_bookmarks_page = 1
    return current_bookmarks_page