"""Provide kiskadee Database operations."""

import kiskadee
from kiskadee.model import Base
from sqlalchemy import create_engine, orm


class Database:
    """kiskadee Database class."""

    def __init__(self, db='db_development'):
        """Return a Database object with SQLAlchemy session and engine."""
        self.engine = self._create_engine(db)
        self.session = self._create_session(self.engine)
        Base.metadata.create_all(self.engine)
        Base.metadata.bind = self.engine

    def _create_engine(self, db):
        driver = kiskadee.config[db]['driver']
        username = kiskadee.config[db]['username']
        password = kiskadee.config[db]['password']
        hostname = kiskadee.config[db]['hostname']
        port = kiskadee.config[db]['port']
        dbname = kiskadee.config[db]['dbname']
        return create_engine('%s://%s:%s@%s:%s/%s' % (driver,
                                                      username,
                                                      password,
                                                      hostname,
                                                      port,
                                                      dbname))

    def _create_session(self, engine):
        DBSession = orm.sessionmaker(bind=engine)
        return DBSession()
