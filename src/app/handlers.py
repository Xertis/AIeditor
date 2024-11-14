from PyQt6 import QtWidgets
from datetime import datetime as dt
from os import path as op
from src.sql.db_tables import recent_files


class Handlers:
    def __init__(self, app):
        self.app = app

    def handler_text_changed(self):
        """ 
        Обработчик, вызываемый после каждого изменения текста в
        файле. Устанавливает флаг, указывающий на то, что данные основного
        текста не были сохранены. 
        """ 
        self.app.if_main_text_data_saved = False

    def handler_select_text(self):
        """
        Обработчик, назначающий новое значение выделенного текста в
        переменную. Сохраняет выделенный текст из основного текстового поля
        в атрибут приложения. 
        """
        self.app.selected_text = self.app.main_text.textCursor().selectedText()

    def handler_load_file(self):
        """
        Обработчик для загрузки файла по выбранному пути. Открывает
        диалог выбора файла и загружает содержимое выбранного файла. 
        """
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.app,
            "Выберите файл",
            "",
            "Text Files (*.txt);;All Files (*)"
        )

        if file_path:
            time_create = dt.fromtimestamp(op.getctime(file_path))
            time_edit = dt.fromtimestamp(op.getmtime(file_path))
            self.handler_save_data()
            file = self.app.db.files.get(
                path=file_path,
                time_create=time_create,
                time_edit=time_edit)
            if file:
                self.app.file = file
            else:
                self.app.file = recent_files()
                self.app.file.path = file_path
                self.app.file.time_create = dt.fromtimestamp(
                    op.getctime(file_path))
                self.app.file.time_edit = dt.fromtimestamp(
                    op.getmtime(file_path))

            self.app.refresh_main_text()
            self.app.refresh_ai_history()

    def handler_save_file(self):
        """
        Обработчик для сохранения открытого файла. Если файл уже был
        загружен, сохраняет его содержимое. В противном случае открывает
        диалог для сохранения нового файла. 
        """
        file_path = self.app.file.path

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.app.main_text.toPlainText())
                self.app.if_main_text_data_saved = True
                file.close()
                self.handler_save_data()
        else:
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.app, "Сохранить файл", "",
                "All Files (*);;Text Files (*.txt)")
            with open(file_path, 'w') as file:
                file.write(self.app.main_text.toPlainText())

    def handler_save_data(self):
        """
        Сохраняет метаданные из текстового файла в бд, если файл не был
        сохранён. Обновляет информацию и сохраняет
        или удаляет данные в зависимости от состояния. 
        """
        file = self.app.file
        if file.path is None:
            return

        file.time_edit = dt.fromtimestamp(op.getmtime(file.path))
        if not self.app.if_main_text_data_saved:
            if not file.id_unsave_data:
                unsave_data = self.app.db.unsave.add(
                    self.app.main_text.toPlainText())
                requests_history = self.app.db.requests.add(
                    self.app.ai_history.toPlainText())

                file.id_unsave_data = unsave_data.id
                file.id_requests_history = requests_history.id
            else:
                unsave_data = self.app.db.unsave.get_by_id(
                    self.app.file.id_unsave_data)
                requests_history = self.app.db.requests.get_by_id(
                    self.app.file.id_requests_history)

                unsave_data.text = self.app.main_text.toPlainText()
                requests_history.text = self.app.ai_history.toPlainText()
        else:
            if file:
                if file.id_unsave_data:
                    self.app.db.unsave.delete_by_id(file.id_unsave_data)
                    print("удаление unsave data")
                if file.id_requests_history:
                    self.app.db.requests.delete_by_id(file.id_requests_history)
                    print("истории переписки из бд")
                self.app.db.files.delete(id=file.id)
                print("удаление файла из бд")
                self.app.db.session.commit()
                return
        self.app.db.session.add(file)
        self.app.db.session.commit()

    def handler_ai_send(self):
        """
        Эта функция переключает режим работы ИИ, выполняет анализ на основе 
        введенного пользователем текста и сохраняет результат в истории. 
        После выполнения анализа очищает текстовое поле для нового ввода 
        и перемещает курсор в области истории.
        """
        self.app.change_ai_mode()

        print(self.app.ai_mode)
        out = self.app.ai_analysis()

        if out:
            request = f"[👤] {self.app.ai_request.toPlainText()}"
            self.app.add_to_history(request, out)
            self.app.ai_request.setPlainText('')
            self.app.move_cursor_down(self.app.ai_history)
