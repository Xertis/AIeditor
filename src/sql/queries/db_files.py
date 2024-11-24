from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from constants import DB_PATH
from src.sql.db_tables import recent_files
from datetime import datetime as dt
from os import path as op

engine = create_engine(DB_PATH)


class DB_recent_files:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_newest(self) -> recent_files:
        """
        Берёт самый новый сохранённый файл из базы
        """
        file = self.session.query(recent_files).order_by(
            recent_files.id.desc()).first()
        return file

    def get_oldest(self) -> recent_files:
        """
        Берёт самый старый сохранённый файл из базы
        """
        file = self.session.query(recent_files).order_by(
            recent_files.id).first()
        return file

    def get(self, path: str, time_create: dt = None,
            time_edit: dt = None) -> recent_files:
        """
        Берёт файл из бд
        """
        file = self.session.query(recent_files).filter(
            recent_files.path == path,
            recent_files.time_create == time_create,
            recent_files.time_edit == time_edit
        ).one_or_none()

        return file

    def get_by_path(self, path: str) -> recent_files:
        """
        Берёт файл по пути из бд
        """
        file = self.session.query(recent_files).filter(
            recent_files.path == path).one_or_none()
        return file

    def update_by_id(self, id: int, id_unsave_data: int = None,
                     id_requests_history: int = None) -> bool:
        """
        Обновляет file по id
        """
        file = self.session.query(recent_files).filter(
            recent_files.id == id).one_or_none()

        if file:
            if id_unsave_data:
                file.id_unsave_data = id_unsave_data
            if id_requests_history:
                file.id_requests_history = id_requests_history

            self.session.commit()
            return True
        else:
            return False

    def delete(self, id=None, path=None) -> None:
        """
        Удаляет файл из дб по id/path\n
        Если id != None, удаляет по айди\n
        Иначе если path != None, удаляет по пути
        """
        file = None

        if id:
            file = self.session.query(recent_files).filter(
                recent_files.id == id).one_or_none()
        elif path:
            file = self.session.query(recent_files).filter(
                recent_files.path == path).one_or_none()

        if file:
            self.session.delete(file)
            self.session.commit()

    def add(self, path: str, id_unsave_data: int = None,
            id_requests_history: int = None) -> recent_files:
        """
        Добавляет новый файл в дб
        """
        if not self.get_file_by_path(path=path):
            file = recent_files(
                path=path,
                id_unsave_data=id_unsave_data,
                id_requests_history=id_requests_history,
                time_create=dt.fromtimestamp(
                    op.getctime(path)),
                time_edit=dt.fromtimestamp(
                    op.getmtime(path)))
            self.session.add(file)
            self.session.commit()
            return file
        else:
            return None
