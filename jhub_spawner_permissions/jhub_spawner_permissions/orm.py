from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError


Base = declarative_base()


class Permission(Base):
    """Permission Table"""

    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    permanent_allow = Column(Boolean(), default=False)
    # Possibly add timestamp


user_permission_map = Table(
    'user_permission_map',
    Base.metadata,
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'),
           primary_key=True),
    Column('permission_id', ForeignKey('permissions.id', ondelete='CASCADE'),
           primary_key=True)
)


class Image(Base):
    """Table for Images"""

    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), default='', unique=True)

    @classmethod
    def find(cls, db, name):
        return db.query(cls).filter(cls.name == name).first()


user_image_map = Table(
    'user_image_map',
    Base.metadata,
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'),
           primary_key=True),
    Column('image_id', ForeignKey('images.id', ondelete='CASCADE'),
           primary_key=True)
)


class User(Base):
    """Table for users"""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True)
    images = relationship('Image', secondary='user_image_map',
                          backref='users')
    permissions = relationship('Permission', secondary='user_permission_map',
                               backref='users')

    @classmethod
    def all(cls, db):
        """Find all users."""
        return db.query(cls).all()

    @classmethod
    def find(cls, db, name):
        """Find a user by name.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.name == name).first()


class DBConnectionManager:

    db = None

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

    def commit(self):
        self.db.commit()
