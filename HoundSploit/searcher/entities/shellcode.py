from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Shellcode(Base):
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
    
    def __init__(self, id, file, description, date, author, exploit_type, platform):
        self.id = id
        self.file = file
        self.description = description
        self.date = date
        self.author = author
        self.type = exploit_type
        self.platform = platform