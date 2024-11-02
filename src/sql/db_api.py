from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from constants import DB_PATH
from src.sql.db_tables import recent_files, unsave_data
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
    
    def get_file_by_path(self, path: str) -> recent_files:
        """
        Берёт файл по пути из бд
        """
        file = self.session.query(recent_files).filter(recent_files.path == path).one_or_none()
        return file
    
    def get_all_files(self) -> List[recent_files]:
        """
        Берёт все сохранённые файлы из базы
        """
        files = self.session.query(recent_files).all()
        return files
    
    def add_file(self, path: str, id_unsave_data: int) -> recent_files:
        """
        Добавляет новый файл в дб
        """
        if not self.get_file_by_path(path=path):
            file = recent_files(path=path, id_unsave_data=id_unsave_data)
            self.session.add(file)
            self.session.commit()
            return file
        else:
            return False
        
    def update_file_by_id(self, id: int, id_unsave_data: int) -> bool:
        """
        Обновляет file по id
        """
        file = self.session.query(recent_files).filter(recent_files.id == id).one_or_none()

        if file:
            file.id_unsave_data = id_unsave_data
            self.session.commit()
            return True
        else:
            return False

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

    def add_unsave_data(self, text) -> unsave_data:
        """
        Добавляет несохранённые данные текстового файла в бд
        """
        data = unsave_data(text=text)
        self.session.add(data)
        self.session.commit()
        return data

    def delete_unsave_data_by_id(self, id) -> None:
        """
        Удаляет несохранённые данные текстового файла из бд
        """
        data = self.session.query(unsave_data).filter(unsave_data.id == id).one_or_none()

        if data:
            self.session.delete(data)
            self.session.commit()

    def update_unsave_data_by_id(self, id: int, text: str) -> bool:
        """
        Обновляет unsave_data по id
        """
        data = self.session.query(unsave_data).filter(unsave_data.id == id).one_or_none()

        if data:
            data.text = text
            self.session.commit()
            return True
        else:
            return False

    def get_unsave_data_by_id(self, id) -> unsave_data:
        """
        Берёт несохранённые данные текстового файла из бд по id
        """
        data = self.session.query(unsave_data).filter(unsave_data.id == id).one_or_none()
        return data

    def session_close(self) -> None:
        """
        Закрывает текущую сессию с бд
        """
        self.session.close()