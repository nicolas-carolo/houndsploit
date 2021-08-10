from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Exploit(Base):
    """
    The database object Exploit
    """
    __tablename__ = 'searcher_exploit'

    id = Column(Integer, primary_key=True)
    file = Column(String)
    description = Column(String)
    date = Column(String)
    author = Column(String)
    type = Column(String)
    platform = Column(String)
    port = Column(Integer)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Shellcode(Base):
    """
    The database object Shellcode
    """
    __tablename__ = 'searcher_shellcode'

    id = Column(Integer, primary_key=True)
    file = Column(String)
    description = Column(String)
    date = Column(String)
    author = Column(String)
    type = Column(String)
    platform = Column(String)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Suggestion(Base):
    """
    The database object Suggestion
    """
    __tablename__ = 'searcher_suggestion'

    searched = Column(String, primary_key=True)
    suggestion = Column(String)
    autoreplacement = Column(String)

    def __init__(self, searched, suggestion, autoreplacement):
        self.searched = searched
        self.suggestion = suggestion
        self.autoreplacement = autoreplacement


class Bookmark(Base):
    """
    The database object Bookmark
    """
    __tablename__ = 'searcher_bookmark'

    vulnerability_id = Column(Integer, primary_key=True)
    vulnerability_class = Column(String, primary_key=True)

    def __init__(self, vulnerability_id, vulnerability_class):
        self.vulnerability_id = vulnerability_id
        self.vulnerability_class = vulnerability_class

