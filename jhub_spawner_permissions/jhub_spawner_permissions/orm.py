import time
from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import Unicode
from sqlalchemy import Interval
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

PACKAGE_NAME = "SpawnerPermissions"

Base = declarative_base()


class AppBase(object):

    @classmethod
    def all(cls, db):
        return db.query(cls).all()

    @classmethod
    def find(cls, db, first=False, **kwargs):
        if first:
            return db.query(cls).filter_by(**kwargs).first()
        else:
            return db.query(cls).filter_by(**kwargs)


class Permission(AppBase, Base):
    """Permission Table"""

    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    allowed = Column(Boolean(), default=False)


class Image(AppBase, Base):
    """Table for Images"""

    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), default='', unique=True)


class UserImagePermissions(AppBase, Base):
    __tablename__ = 'user_image_permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    image_id = Column(Integer, ForeignKey('images.id', ondelete='CASCADE'))
    permission_id = Column(Integer, ForeignKey('permissions.id', ondelete='CASCADE'))

    user = relationship('User')
    image = relationship('Image')
    permission = relationship('Permission')


class User(AppBase, Base):
    """Table for users"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True)


class DBConnectionManager:

    db = None

    # TODO, add logger
    def __init__(self, url="sqlite:///jupyterhub.sqlite:", **kwargs):
        try:
            engine = create_engine(url, **kwargs)
            Base.metadata.create_all(engine)
            session_factory = sessionmaker(bind=engine)
            self.db = session_factory()
        except OperationalError as e:
            print("Database error {}".format(e))

    def add(self, obj):
        self.db.add(obj)

    def add_all(self, obj):
        self.db.add_all(obj)

    def commit(self):
        try:
            self.db.commit()
        except Exception as err:
    #        logger.error("{} - failed to execute db commit, err: {}".format(PACKAGE_NAME, err))
            return False
        return True

    def close(self):
        self.db.close()
