"""Establish data / cache file paths, and configurations,
bootstrap fixture data if necessary.

"""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


# scoped_session.
Session = scoped_session(sessionmaker())

# global declarative base class.
Base = declarative_base()

root = "./data/"

dbfile = os.path.join(root, "demo.db")
engine = create_engine("sqlite:///%s" % dbfile, echo=True)
Session.configure(bind=engine)
