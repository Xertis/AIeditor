import sys
from PyQt6 import QtWidgets, uic
from PyQt6 import QtWidgets, QtGui
from src.ai_requests import AI
from src.sql.db_api import DB
import os

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Инициализация главного окна
        """
        super(MyApp, self).__init__()
        uic.loadUi('main.ui', self)

        self.ai = AI()
        self.db = DB()

        self.ai_mode = self.ai.QA

        self.file_path = ''
        file = self.db.get_newest_file()
        if file:
            self.file_path = file.path

        self.ai_chat_context = []
        self.if_main_text_data_saved = True

        self.refresh_main_text()
        self.load_connections()
        self.load_ui()

    def closeEvent(self, event):
        """
        Сохраняет данные из текстового файла, если файл не был сохранён
        """
        if not self.if_main_text_data_saved:
            unsave_data = self.db.add_unsave_data(self.main_text.toPlainText())
            if unsave_data:
                f = self.db.add_file(path=self.file_path, id_unsave_data=unsave_data.id)
                if not f:
                    f = self.db.get_file_by_path(path=self.file_path)
                    self.db.delete_unsave_data_by_id(id=f.id_unsave_data)
                    self.db.update_file_by_id(id=f.id, id_unsave_data=unsave_data.id)
        else:
            file = self.db.get_file_by_path(path=self.file_path)

            if file.id_unsave_data:
                unsave_data = self.db.get_unsave_data_by_id(id=file.id_unsave_data)
                self.db.delete_unsave_data_by_id(unsave_data.id)
                print("удаление unsave data")
            self.db.delete_file(id=file.id)
            print("удаление файла из бд")
            


    def load_connections(self):
        """
        Подключение всех кнопок к их хендлерам
        """
        self.open_file.clicked.connect(self.handler_load_file)
        self.ai_send_button.clicked.connect(self.handler_ai_send)
        self.main_text.selectionChanged.connect(self.handler_select_text)
        self.main_text.textChanged.connect(self.handler_text_changed)
        self.save_file.clicked.connect(self.handler_save_file)

    def refresh_main_text(self):
        """
        Обновляет main_text данными из файла
        """
        file_path = self.file_path

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                f = self.db.get_file_by_path(path=file_path)
                if f:
                    unsave_data = self.db.get_unsave_data_by_id(id=f.id_unsave_data)
                    if unsave_data:
                        text = unsave_data.text
                        self.if_main_text_data_saved = False

                self.main_text.setPlainText(text)
                file.close()

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

    def handler_text_changed(self):
        self.if_main_text_data_saved = False

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
        
        self.file_path = file_path
        self.refresh_main_text()

    def handler_save_file(self):
        """
        Сохраняет открытый файл
        """
        file_path = self.file_path

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.main_text.toPlainText())
                self.if_main_text_data_saved = True
                file.close()

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
