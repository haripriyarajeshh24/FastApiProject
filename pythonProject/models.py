from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,  index=True)
    signup = Column(String)
    login = Column(String)


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    # user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    #
    # user = relationship('Users', back_populates='posts')
