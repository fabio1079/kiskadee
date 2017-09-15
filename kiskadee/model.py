"""This module provides kiskadee database model."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, UnicodeText, UniqueConstraint,\
                       Sequence, Unicode, ForeignKey, orm, JSON
import kiskadee

Base = declarative_base()

"""class TypeEnum(enum.Enum):
    Enum for to use on TypeReport class
    error = 1
    style = 2
    warning = 3"""

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
    report = orm.relationship('Reports', backref='analysis')

class Reports(Base):
    """Abstraction of a analysis report"""
    __tablename__ = 'reports'
    id = Column(Integer,
                Sequence('reports_id_seq', optional=True), primary_key=True)
    report_type = Column(Unicode(100), nullable=False)
    counter = Column(Integer)
    analysis_id = Column(Integer, ForeignKey('analysis.id'), nullable=False)

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
