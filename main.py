import sys
from PyQt6 import QtWidgets, uic
from PyQt6 import QtWidgets, QtGui
from src.ai_requests import AI
from src.sql.db_api import DB

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Инициализация главного окна
        """
        super(MyApp, self).__init__()
        uic.loadUi('main.ui', self)

        self.load_connections()
        self.load_ui()

        self.ai = AI()
        self.db = DB()

        self.ai_mode = self.ai.QA
        self.ai_chat_context = []

    def load_connections(self):
        """
        Подключение всех кнопок к их хендлерам
        """
        self.open_file.clicked.connect(self.handler_load_file)
        self.ai_send_button.clicked.connect(self.handler_ai_send)
        self.main_text.selectionChanged.connect(self.handler_select_text)

    def load_ui(self):
        """
        Загрузка настроек интерфейса
        """
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
            
            out = self.ai.question_answering(self.ai_request.toPlainText(), self.main_text.toPlainText())
        elif self.ai_mode == self.ai.SUMMARING:
            if len(self.selected_text) == 0:
                return False
            
            try:
                out = self.ai.summaring(self.selected_text, int(self.ai_request.toPlainText()))
            except (ValueError) as e:
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

    def handler_select_text(self):
        """
        Назначает новое значение выделенного текста в переменную
        """
        self.selected_text = self.main_text.textCursor().selectedText()

    def handler_load_file(self):
        """
        Загружает файл по выбранному пути
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                self.main_text.setPlainText(text)
                self.db.add_file(file_path)

    def handler_ai_send(self):
        """
        Отправляет в нейронку сообщение пользователя
        """
        self.change_ai_mode()

        print(self.ai_mode)
        out = self.ai_analysis()

        if out:
            request = f"[👤] {self.ai_request.toPlainText()}"
            self.add_to_history(request, out)
            self.ai_request.setPlainText('')
            self.move_cursor_down(self.ai_history)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
