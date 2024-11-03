import sys
from PyQt6 import QtWidgets, uic
from PyQt6 import QtWidgets, QtGui
from src.ai_requests import AI
from src.sql.db_api import DB
import os

class Handlers:

    def __init__(self, app):
        self.app = app

    def handler_text_changed(self):
        """
        Вызывается после каждого изменения файла
        """
        self.app.if_main_text_data_saved = False

    def handler_select_text(self):
        """
        Назначает новое значение выделенного текста в переменную
        """
        self.app.selected_text = self.app.main_text.textCursor().selectedText()

    def handler_load_file(self):
        """
        Загружает файл по выбранному пути
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.app,
            "Выберите файл",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        self.app.file_path = file_path
        self.app.refresh_main_text()

    def handler_save_file(self):
        """
        Сохраняет открытый файл
        """
        file_path = self.app.file_path

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.app.main_text.toPlainText())
                self.app.if_main_text_data_saved = True
                file.close()

    def handler_ai_send(self):
        """
        Отправляет в нейронку сообщение пользователя
        """
        self.app.change_ai_mode()

        print(self.app.ai_mode)
        out = self.app.ai_analysis()

        if out:
            request = f"[👤] {self.app.ai_request.toPlainText()}"
            self.app.add_to_history(request, out)
            self.app.ai_request.setPlainText('')
            self.app.move_cursor_down(self.app.ai_history)