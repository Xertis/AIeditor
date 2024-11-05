from sqlalchemy import create_engine, Column, Integer, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from constants import DB_PATH

engine = create_engine(DB_PATH)
Base = declarative_base()

class unsave_data(Base):
    __tablename__ = "unsave_data"

    id = Column(Integer, primary_key=True)
    text = Column(Text)

class requests_history(Base):
    __tablename__ = "requests_history"

    id = Column(Integer, primary_key=True)
    text = Column(Text)

class recent_files(Base):
    __tablename__ = "recent_files"
    
    id = Column(Integer, primary_key=True)
    path = Column(Text)
    id_unsave_data = Column(Integer, ForeignKey("unsave_data.id"))
    id_requests_history = Column(Integer, ForeignKey("requests_history.id"))
    time_create = Column(TIMESTAMP)
    time_edit = Column(TIMESTAMP)

Base.metadata.create_all(engine)
