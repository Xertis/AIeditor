import os
from PyQt6 import uic, QtGui
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction
from src.ai_requests import AI
from src.sql.db_api import DB
from src.app.handlers import Handlers
from src.sql.db_tables import recent_files


class Aieditor(QMainWindow):
    def __init__(self):
        super(Aieditor, self).__init__()
        self.load_ui()
        self.ai = AI()
        self.db = DB()

        self.handlers = Handlers(self)

        self.ai_mode = self.ai.QA
        self.file = self.db.files.get_newest()
        self.file = self.file if self.file else recent_files()

        self.ai_chat_context = []
        self.if_main_text_data_saved = False if \
            self.file.id_unsave_data else True

        self.refresh_main_text()
        self.refresh_ai_history()
        self.load_connections()

    def load_ui(self):
        """
        Этот метод отвечает за загрузку настроек пользовательского
        интерфейса при старте приложения.
        """
        uic.loadUi('main.ui', self)
        self.setWindowTitle("AIeditor")
        self.ai_history.setReadOnly(True)
        self.selected_text = ""

    def closeEvent(self, event):
        """
        Этот метод вызывается при закрытии приложения. Внутри него
        происходит сохранение текущих данных приложения, чтобы
        при следующем запуске пользователь мог продолжить с того места, где
        остановился.
        """
        self.handlers.handler_save_data()
        self.db.session.close()

    def load_connections(self):
        """
        Метод отвечает за связывание элементов интерфейса,
        чтобы при нажатии на кнопку выполнялась
        определенная функция.
        """
        self.ai_send_button.clicked.connect(self.handlers.handler_ai_send)
        self.main_text.selectionChanged.connect(
            self.handlers.handler_select_text)
        self.main_text.textChanged.connect(self.handlers.handler_text_changed)

        open_action = QAction("Open file", self)
        open_action.triggered.connect(self.handlers.handler_load_file)
        self.toolbar.addAction(open_action)

        save_action = QAction("Save file", self)
        save_action.triggered.connect(self.handlers.handler_save_file)
        self.toolbar.addAction(save_action)

    def refresh_main_text(self):
        """
        Этот метод обновляет текстовое поле в главном интерфейсе
        приложения, загружая данные из файла или бд.
        """
        file_path = self.file.path if self.file.path else ''

        if self.file.id_unsave_data:
            unsave_data = self.db.unsave.get_by_id(self.file.id_unsave_data)
            self.main_text.setPlainText(unsave_data.text)
            return

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
        """
        Метод обновляет историю взаимодействий с искусственным
        интеллектом. Он может загружать предыдущие запросы и ответы
        из базы данных или файла, чтобы пользователь мог видеть,
        какие вопросы он задавал и какие ответы получал.
        """
        file = self.file

        if file and file.id_requests_history:
            history = self.db.requests.get_by_id(file.id_requests_history).text
            self.ai_history.setPlainText(history)
            self.ai_chat_context = history.split('\n')
        else:
            self.ai_history.setPlainText('')
            self.ai_chat_context.clear()

    def ai_analysis(self):
        """
        Метод запускает процесс анализа текста с использованием
        нейронной сети. Входные
        данные могут поступать от пользователя, а результат анализа
        возвращается и
        отображается в интерфейсе приложения.
        """
        out = ''
        if self.ai_mode == self.ai.QA:
            if len(self.ai_request.toPlainText()) == 0:
                return ''
            if len(self.main_text.toPlainText()) == 0:
                return ''

            out = self.ai.question_answering(
                self.ai_request.toPlainText(),
                self.main_text.toPlainText())
        elif self.ai_mode == self.ai.SUMMARING:
            if len(self.selected_text) == 0:
                return ''

            if self.ai_request.toPlainText().isnumeric():
                out = self.ai.summaring(
                    self.selected_text,
                    int(self.ai_request.toPlainText())
                )
            else:
                out = self.ai.summaring(self.selected_text)

        return f"[🤖] {out}"

    def change_ai_mode(self):
        """
        Этот метод позволяет переключать режимы работы
        искусственного интеллекта, такие как "суммаризация и "QA", этот метод
        управляет изменением текущего
        режима в зависимости от потребностей пользователя.
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
        Метод добавляет текстовые сообщения в историю диалога с
        искусственным интеллектом. Это может включать как запросы
        пользователя, так и ответы ИИ.
        """
        for text in texts:
            self.ai_chat_context.append(text)
        self.ai_history.setPlainText('\n'.join(self.ai_chat_context))

    def move_cursor_down(self, t):
        """
        Метод позволяет прокручивать выбранное текстовое поле в самый низ
        """
        cursor = QtGui.QTextCursor(t.document())
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
        t.setTextCursor(cursor)
