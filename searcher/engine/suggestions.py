from searcher.db_manager.models import Suggestion
from searcher.db_manager.session_manager import start_session
from searcher.db_manager.result_set import queryset2list


def substitute_with_suggestions(searched_text):
    """
    Substitute automatically an user's input with an appropriate suggestion.
    :param searched_text: the user's input.
    :return: the new input to use for the search.
    """
    session = start_session()
    suggestions = session.query(Suggestion)
    session.close()
    for suggested_word in suggestions:
        if searched_text.lower().__contains__(suggested_word.searched.lower())\
                and suggested_word.autoreplacement == 'true' \
                and not str(searched_text).lower().__contains__(suggested_word.suggestion.lower()):
            searched_text = str(searched_text.lower()).replace(suggested_word.searched.lower(),
                                                               suggested_word.suggestion.lower())
    print(searched_text)
    return searched_text


def propose_suggestions(searched_text):
    """
    Suggest to the user a related search that he can do.
    :param searched_text: the user's input.
    :return: the suggested search.
    """
    suggested_searched_text = ''
    session = start_session()
    queryset = session.query(Suggestion)
    suggestions = queryset2list(queryset)
    session.close()
    for suggested_word in suggestions:
        if searched_text.lower().__contains__(suggested_word.searched.lower()) \
                and suggested_word.autoreplacement == 'false' \
                and not str(searched_text).lower().__contains__(suggested_word.suggestion.lower()):
            suggested_searched_text = str(searched_text.lower()).replace(suggested_word.searched.lower(),
                                                                     suggested_word.suggestion.lower())
    return suggested_searched_text
