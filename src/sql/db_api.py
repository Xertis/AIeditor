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
    
    def add_file(self, path: str) -> None:
        """
        Добавляет новый файл в дб
        """
        self.session.add(recent_files(path=path))
        self.session.commit()

    def delete_file(self, id=None, path=None) -> None:
        """
        Удаляет файл из дб по id/path\n
        Если id != None, удаляет по айди\n
        Иначе если path != None, удаляет по пути
        """
        file = None

        if id:
            file = self.session.query(recent_files).filter(recent_files.id == id).one_or_none()
        elif path:
            file = self.session.query(recent_files).filter(recent_files.path == path).one_or_none()

        if file:
            self.session.delete(file)
            self.session.commit()