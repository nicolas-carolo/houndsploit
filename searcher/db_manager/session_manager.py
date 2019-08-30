import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session


def start_session():
    """
    Start a new database session.
    :return: a new database session.
    """
    engine = sqlalchemy.create_engine('sqlite:///hound_db.sqlite3', connect_args={'check_same_thread': False})
    Session = sessionmaker(bind=engine)
    return Session()
