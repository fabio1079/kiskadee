"""This module provides kiskadee database model."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, UnicodeText, UniqueConstraint,\
                       Sequence, Unicode, ForeignKey, orm, JSON, String
from passlib.apps import custom_app_context as pwd_context
import kiskadee

Base = declarative_base()


class Package(Base):
    """Software packages abstraction.

    A software package is the source code for a software project. It may be
    upstream's distribution or the sources provided by some other source, like
    a linux distribution.
    """

    __tablename__ = 'packages'
    id = Column(Integer,
                Sequence('packages_id_seq', optional=True), primary_key=True)
    name = Column(Unicode(255), nullable=False)
    homepage = Column(Unicode(255), nullable=True)
    fetcher_id = Column(Integer, ForeignKey('fetchers.id'), nullable=False)
    versions = orm.relationship('Version', backref='packages')
    __table_args__ = (
            UniqueConstraint('name', 'fetcher_id'),
            )


class Fetcher(Base):
    """kiskadee fetcher abstraction."""

    __tablename__ = 'fetchers'
    id = Column(Integer,
                Sequence('fetchers_id_seq', optional=True), primary_key=True)
    name = Column(Unicode(255), nullable=False, unique=True)
    target = Column(Unicode(255), nullable=True)
    description = Column(UnicodeText)
    packages = orm.relationship('Package', backref='fetchers')


class Version(Base):
    """Abstraction of a package version."""

    __tablename__ = 'versions'
    id = Column(Integer,
                Sequence('versions_id_seq', optional=True), primary_key=True)
    number = Column(Unicode(100), nullable=False)
    package_id = Column(Integer, ForeignKey('packages.id'), nullable=False)
    analysis = orm.relationship('Analysis', backref='versions')
    __table_args__ = (
            UniqueConstraint('number', 'package_id'),
            )


class Analyzer(Base):
    """Abstraction of a static analyzer."""

    __tablename__ = 'analyzers'
    id = Column(Integer,
                Sequence('analyzers_id_seq', optional=True), primary_key=True)
    name = Column(Unicode(255), nullable=False, unique=True)
    version = Column(Unicode(255), nullable=True)
    analysis = orm.relationship('Analysis', backref='analyzers')


class Analysis(Base):
    """Abstraction of a package analysis."""

    __tablename__ = 'analysis'
    id = Column(Integer,
                Sequence('analysis_id_seq', optional=True), primary_key=True)
    version_id = Column(Integer, ForeignKey('versions.id'), nullable=False)
    analyzer_id = Column(Integer, ForeignKey('analyzers.id'), nullable=False)
    raw = Column(JSON)
    report = orm.relationship('Report',
                              uselist=False, back_populates='analysis')


class Report(Base):
    """Abstraction of a analysis report."""

    __tablename__ = 'reports'
    id = Column(Integer,
                Sequence('reports_id_seq', optional=True), primary_key=True)
    analysis_id = Column(Integer, ForeignKey('analysis.id'), nullable=False)
    results = Column(JSON)
    analysis = orm.relationship('Analysis', back_populates='report')


def create_analyzers(_session):
    """Create the analyzers on database.

    The kiskadee analyzers are defined on the section `analyzers` of the
    kiskadee.conf file. The `_session` argument represents a sqlalchemy
    session.
    """
    list_of_analyzers = dict(kiskadee.config._sections["analyzers"])
    for name, version in list_of_analyzers.items():
        if not (_session.query(Analyzer).filter(Analyzer.name == name).
                filter(Analyzer.version == version).first()):
            new_analyzer = kiskadee.model.Analyzer()
            new_analyzer.name = name
            new_analyzer.version = version
            _session.add(new_analyzer)
    _session.commit()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,
                Sequence('users_id_seq', optional=True), primary_key=True)
    name = Column(Unicode(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(128))

    def hash_password(self, password):
        """Takes a plain password as argument
        and stores a hash of it with the user.
        """
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        """Takes a plain password as argument and returns
        True if the password is correct
        False if not.
        """
        return pwd_context.verify(password, self.password_hash)
