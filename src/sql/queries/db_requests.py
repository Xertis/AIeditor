from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from constants import DB_PATH
from src.sql.db_tables import requests_history

engine = create_engine(DB_PATH)


class DB_requests_history:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, text: str) -> requests_history:
        """
        Добавляет историю переписки с AI в бд
        """
        data = requests_history(text=text)
        self.session.add(data)
        self.session.commit()
        return data

    def get_by_id(self, id: int) -> requests_history:
        """
        Берёт историю переписки с AI из бд по id
        """
        data = self.session.query(requests_history).filter(
            requests_history.id == id).one_or_none()
        return data

    def delete_by_id(self, id: int) -> None:
        """
        Удаляет историю переписки с AI из бд
        """

        data = self.session.query(requests_history).filter(
            requests_history.id == id).one_or_none()

        if data:
            self.session.delete(data)
            self.session.commit()
