from searcher.models import Suggestion


def substitute_with_suggestions(search_text):
    """
    Substitute automatically an user's input with an appropriate suggestion.
    :param search_text: the user's input.
    :return: the new input to use for the search.
    """
    suggestions = Suggestion.objects.all()
    for suggested_word in suggestions:
        if search_text.lower().__contains__(suggested_word.searched.lower())\
                and suggested_word.autoreplacement is True \
                and not str(search_text).lower().__contains__(suggested_word.suggestion.lower()):
            search_text = str(search_text.lower()).replace(suggested_word.searched.lower(),
                                                           suggested_word.suggestion.lower())
    return search_text


def propose_suggestions(search_text):
    """
    Suggest to the user a related search that he can do.
    :param search_text: the user's input.
    :return: the suggested search.
    """
    suggested_search_text = ''
    suggestions = Suggestion.objects.all()
    for suggested_word in suggestions:
        if search_text.lower().__contains__(suggested_word.searched.lower()) \
                and suggested_word.autoreplacement is False \
                and not str(search_text).lower().__contains__(suggested_word.suggestion.lower()):
            suggested_search_text = str(search_text.lower()).replace(suggested_word.searched.lower(),
                                                                     suggested_word.suggestion.lower())
    return suggested_search_text
