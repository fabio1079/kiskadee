"""Provide kiskadee Database operations."""

import kiskadee
from sqlalchemy import create_engine, orm


class Database:
    """kiskadee Database class."""

    def __init__(self):
        """Return a Database object with SQLAlchemy session and engine."""
        self.engine = self._create_engine()
        self.session = self._create_session(self.engine)

    def _create_engine(self):
        driver = kiskadee.config['db']['driver']
        username = kiskadee.config['db']['username']
        password = kiskadee.config['db']['password']
        hostname = kiskadee.config['db']['hostname']
        port = kiskadee.config['db']['port']
        dbname = kiskadee.config['db']['dbname']
        return create_engine('%s://%s:%s@%s:%s/%s' % (driver,
                                                      username,
                                                      password,
                                                      hostname,
                                                      port,
                                                      dbname))

    def _create_session(self, engine):
        DBSession = orm.sessionmaker(bind=engine)
        return DBSession()
