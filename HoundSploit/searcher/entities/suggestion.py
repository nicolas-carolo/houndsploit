from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from HoundSploit.searcher.utils.string import string_contains

Base = declarative_base()


class Suggestion(Base):
    __tablename__ = 'searcher_suggestion'

    searched = Column(String, primary_key=True)
    suggestion = Column(String)
    autoreplacement = Column(String)

    def __init__(self, searched, suggestion, autoreplacement):
        self.searched = searched
        self.suggestion = suggestion
        self.autoreplacement = autoreplacement


    def is_eligible(self, searched_text):
        if string_contains(searched_text, self.searched) and not string_contains(self.suggestion, searched_text):
            return True
        else:
            return False


    def replace_searched_text_with_suggestion(self, searched_text):
        searched_text = str(searched_text).lower()
        old_word = str(self.searched).lower()
        new_word = str(self.suggestion).lower()
        searched_text = searched_text.replace(old_word, new_word)
        return searched_text