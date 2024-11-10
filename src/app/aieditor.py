import os
from PyQt6 import QtWidgets, uic, QtGui
from src.ai_requests import AI
from src.sql.db_api import DB
from src.app.handlers import Handlers
from src.sql.db_tables import recent_files


class Aieditor(QtWidgets.QMainWindow):
    def __init__(self):
        super(Aieditor, self).__init__()
        self.load_ui()
        self.ai = AI()
        self.db = DB()

        self.handlers = Handlers(self)

        self.ai_mode = self.ai.QA
        self.file = self.db.files.get_newest(
        ) if self.db.files.get_newest() else recent_files()
        self.ai_chat_context = []
        self.if_main_text_data_saved = True
        self.refresh_main_text()
        self.refresh_ai_history()
        self.load_connections()

    def closeEvent(self, event):
        self.handlers.handler_save_data()

    def load_connections(self):
        """
        Подключение всех кнопок к их хендлерам
        """
        self.open_file.clicked.connect(self.handlers.handler_load_file)
        self.ai_send_button.clicked.connect(self.handlers.handler_ai_send)
        self.main_text.selectionChanged.connect(
            self.handlers.handler_select_text)
        self.main_text.textChanged.connect(self.handlers.handler_text_changed)
        self.save_file.clicked.connect(self.handlers.handler_save_file)

    def refresh_main_text(self):
        """
        Обновляет main_text данными из файла
        """
        file_path = self.file.path if self.file.path else ''

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                f = self.db.files.get_by_path(path=file_path)
                if f:
                    unsave_data = self.db.unsave.get_by_id(id=f.id_unsave_data)
                    if unsave_data:
                        text = unsave_data.text
                        self.if_main_text_data_saved = False

                self.main_text.setPlainText(text)
                file.close()
        else:
            self.main_text.setPlainText('')

    def refresh_ai_history(self):
        file = self.file

        if file and file.id_requests_history:
            history = self.db.requests.get_by_id(file.id_requests_history).text
            self.ai_history.setPlainText(history)
            self.ai_chat_context = history.split('\n')
        else:
            self.ai_history.setPlainText('')
            self.ai_chat_context.clear()

    def load_ui(self):
        """
        Загрузка настроек интерфейса
        """
        uic.loadUi('main.ui', self)
        self.ai_history.setReadOnly(True)
        self.selected_text = ""

    def ai_analysis(self):
        """
        Анализирует нейронкой текст
        """
        out = False
        if self.ai_mode == self.ai.QA:
            if len(self.ai_request.toPlainText()) == 0:
                return False
            if len(self.main_text.toPlainText()) == 0:
                return False

            out = self.ai.question_answering(
                self.ai_request.toPlainText(),
                self.main_text.toPlainText())
        elif self.ai_mode == self.ai.SUMMARING:
            if len(self.selected_text) == 0:
                return False

            try:
                out = self.ai.summaring(
                    self.selected_text, int(
                        self.ai_request.toPlainText()))
            except (ValueError):
                out = self.ai.summaring(self.selected_text)

        return f"[🤖] {out}"

    def change_ai_mode(self):
        """
        Меняет режим, в котором щас работает ИИ
        (по факту меняет нейронку, которая щас будет работать)
        """
        request = self.ai_request.toPlainText().strip()

        if request.isnumeric():
            self.ai_mode = self.ai.SUMMARING
            return
        if len(request) == 0:
            self.ai_mode = self.ai.SUMMARING
            return

        self.ai_mode = self.ai.QA

    def add_to_history(self, *texts):
        """
        Добавляет текст в историю диалога с нейронкой
        """
        for text in texts:
            self.ai_chat_context.append(text)
        self.ai_history.setPlainText('\n'.join(self.ai_chat_context))

    def move_cursor_down(self, t):
        """
        Прокручивает до низа менюшку
        """
        cursor = QtGui.QTextCursor(t.document())
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
        t.setTextCursor(cursor)
