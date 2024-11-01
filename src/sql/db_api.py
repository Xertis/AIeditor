from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from constants import DB_PATH
from src.sql.db_tables import recent_files

engine = create_engine(DB_PATH)

class DB:
    def __init__(self) -> None:
        self.session = sessionmaker(bind=engine)()

    def get_latest_file(self) -> recent_files:
        file = self.session.query(recent_files).order_by(recent_files.id.desc()).first()
        return file