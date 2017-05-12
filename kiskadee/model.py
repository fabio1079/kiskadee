from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, UnicodeText, UniqueConstraint,\
                       Sequence, Unicode, ForeignKey, Boolean, orm,\
                       create_engine

Base = declarative_base()


class Package(Base):
    __tablename__ = 'packages'
    id = Column(Integer, Sequence('packages_id_seq', optional=True), primary_key=True)
    name = Column(Unicode(255), nullable=False)
    plugin_id = Column(Integer, ForeignKey('plugins.id'), nullable=False)
    versions = orm.relationship('Version', backref='packages')
    __table_args__ = (
            UniqueConstraint('name', 'plugin_id'),
            )


class Plugin(Base):
    __tablename__ = 'plugins'
    id = Column(Integer, Sequence('plugins_id_seq', optional=True), primary_key=True)
    name = Column(Unicode(255), nullable=False, unique=True)
    target = Column(Unicode(255), nullable=False)
    description = Column(UnicodeText)
    packages = orm.relationship('Package', backref='plugins')


class Version(Base):
    __tablename__ = 'versions'
    id = Column(Integer, Sequence('versions_id_seq', optional=True), primary_key=True)
    number = Column(Unicode(100), nullable=False)
    package_id = Column(Integer, ForeignKey('packages.id'), nullable=False)
    has_analysis = Column(Boolean)
    analysis = Column(UnicodeText)
    __table_args__ = (
            UniqueConstraint('number', 'package_id'),
            )
