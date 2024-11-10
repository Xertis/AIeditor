from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from constants import DB_PATH
from src.sql.db_tables import unsave_data

engine = create_engine(DB_PATH)


class DB_unsave:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, text) -> unsave_data:
        """
        Добавляет несохранённые данные текстового файла в бд
        """
        data = unsave_data(text=text)
        self.session.add(data)
        self.session.commit()
        return data

    def delete_by_id(self, id) -> None:
        """
        Удаляет несохранённые данные текстового файла из бд
        """
        data = self.session.query(unsave_data).filter(
            unsave_data.id == id).one_or_none()

        if data:
            self.session.delete(data)
            self.session.commit()

    def update_by_id(self, id: int, text: str) -> bool:
        """
        Обновляет unsave_data по id
        """
        data = self.session.query(unsave_data).filter(
            unsave_data.id == id).one_or_none()

        if data:
            data.text = text
            self.session.commit()
            return True
        else:
            return False

    def get_by_id(self, id) -> unsave_data:
        """
        Берёт несохранённые данные текстового файла из бд по id
        """
        data = self.session.query(unsave_data).filter(
            unsave_data.id == id).one_or_none()
        return data
