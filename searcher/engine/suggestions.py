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


def get_suggestions_list():
    """
    Get all suggestions in the database
    :return: a list containing all suggestions
    """
    session = start_session()
    queryset = session.query(Suggestion)
    suggestions_list = queryset2list(queryset)
    session.close()
    return suggestions_list


def new_suggestion(searched, suggestion, autoreplacement):
    session = start_session()
    searched = str(searched).lower()
    suggestion = str(suggestion).lower()
    queryset = session.query(Suggestion).filter(Suggestion.searched == searched)
    results_list = queryset2list(queryset)
    if len(results_list) == 0:
        new_suggestion = Suggestion(searched, suggestion, autoreplacement)
        session.add(new_suggestion)
    else:
        edited_suggestion = session.query(Suggestion).get(searched)
        edited_suggestion.suggestion = suggestion
        edited_suggestion.autoreplacement = autoreplacement
    session.commit()
    session.close()


def remove_suggestion(searched):
    session = start_session()
    suggestion_item = session.query(Suggestion).get(searched)
    if suggestion_item is not None:
        session.query(Suggestion).filter(Suggestion.searched == searched).delete()
        session.commit()
        session.close()
        return True
    else:
        return False
