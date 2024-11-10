from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from constants import DB_PATH

from src.sql.queries.db_files import DB_recent_files
from src.sql.queries.db_requests import DB_requests_history
from src.sql.queries.db_unsave import DB_unsave

engine = create_engine(DB_PATH)


class DB:
    def __init__(self) -> None:
        self.session = sessionmaker(bind=engine)()

        self.files = DB_recent_files(self.session)
        self.unsave = DB_unsave(self.session)
        self.requests = DB_requests_history(self.session)

    def session_close(self) -> None:
        """
        Закрывает текущую сессию с бд
        """
        self.session.close()
