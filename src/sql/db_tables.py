from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from constants import DB_PATH

engine = create_engine(DB_PATH)
Base = declarative_base()

class recent_files(Base):
    __tablename__ = "recent_files"
    
    id = Column(Integer, primary_key=True)
    path = Column(Text)

Base.metadata.create_all(engine)
