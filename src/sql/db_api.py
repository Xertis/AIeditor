from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from constants import DB_PATH
from src.sql.db_tables import recent_files
from typing import List

engine = create_engine(DB_PATH)

class DB:
    def __init__(self) -> None:
        self.session = sessionmaker(bind=engine)()

    def get_newest_file(self) -> recent_files:
        """
        Берёт самый новый сохранённый файл из базы
        """
        file = self.session.query(recent_files).order_by(recent_files.id.desc()).first()
        return file
    
    def get_oldest_file(self) -> recent_files:
        """
        Берёт самый старый сохранённый файл из базы
        """
        file = self.session.query(recent_files).order_by(recent_files.id).first()
        return file
    
    def get_all_files(self) -> List[recent_files]:
        """
        Берёт все сохранённые файлы из базы
        """
        files = self.session.query(recent_files).all()
        return files