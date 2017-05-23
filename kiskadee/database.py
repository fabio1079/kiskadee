from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, orm

class Database:
    def __init__(self):
        self.engine = self._create_engine()
        self.session = self._create_session(self.engine)

    def _create_engine(self):
        return create_engine('postgresql://kiskadee:kiskadee@localhost/kiskadee')

    def _create_session(self, engine):
        DBSession = orm.sessionmaker(bind=engine)
        return DBSession()
