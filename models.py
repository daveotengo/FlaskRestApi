from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import JSONType

engine = create_engine('mysql+pymysql://root:Dadapapa4141@localhost:3306/alch_db?charset=utf8mb4', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()

# We will need this for querying
Base.query = db_session.query_property()
#   id = Column(Integer, primary_key=True)
#   name = Column(String)

class Video(Base):
    __tablename__ = 'video_model'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    views = Column(String)
    likes = Column(String)

    def __repr__(self):
        return "Video(name={name},views={views},likes={likes})"


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer,primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"Department(name={self.name})"