from PyQt6 import QtWidgets
from datetime import datetime as dt
from os import path as op

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
        time_create = dt.fromtimestamp(op.getctime(file_path))
        time_edit = dt.fromtimestamp(op.getmtime(file_path))
        file = self.app.db.get_file(path=file_path, time_create=time_create, time_edit=time_edit)
        if file:
            self.app.file = file
        else:
            self.app.file.path = file_path
            self.app.file.time_create = dt.fromtimestamp(op.getctime(file_path))
            self.app.file.time_edit = dt.fromtimestamp(op.getmtime(file_path))

        self.app.refresh_main_text()

    def handler_save_file(self):
        """
        Сохраняет открытый файл
        """
        file_path = self.app.file.path

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.app.main_text.toPlainText())
                self.app.if_main_text_data_saved = True
                file.close()
                self.handler_save_data()

    def handler_save_data(self):
        """
        Сохраняет данные из текстового файла, если файл не был сохранён
        """
        if not self.app.if_main_text_data_saved:
            unsave_data = self.app.db.add_unsave_data(self.app.main_text.toPlainText())
            requests_history = self.app.db.add_requests_history(self.app.ai_history.toPlainText())

            self.app.file.id_unsave_data = unsave_data.id
            self.app.file.id_requests_history = requests_history.id

            self.app.db.session.add(self.app.file)
            self.app.db.session.commit()
        else:
            file = self.app.db.get_file_by_path(path=self.app.file.path)
            
            if file:
                if file.id_unsave_data:
                    self.app.db.delete_unsave_data_by_id(file.id_unsave_data)
                    print("удаление unsave data")
                if file.id_requests_history:
                    self.app.db.delete_requests_history_by_id(file.id_requests_history)
                    print("истории переписки из бд")
                self.app.db.delete_file(id=file.id)
                print("удаление файла из бд")

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