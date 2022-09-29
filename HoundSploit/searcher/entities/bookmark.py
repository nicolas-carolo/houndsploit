from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bookmark(Base):
    __tablename__ = 'searcher_bookmark'

    vulnerability_id = Column(Integer, primary_key=True)
    vulnerability_class = Column(String, primary_key=True)
    date = Column(DateTime)

    def __init__(self, vulnerability_id, vulnerability_class, date):
        self.vulnerability_id = vulnerability_id
        self.vulnerability_class = vulnerability_class
        self.date = date