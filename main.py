import sys
from PyQt6 import QtWidgets, uic
from PyQt6 import QtWidgets, QtGui


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('main.ui', self)

        self.open_file.clicked.connect(self.load_file)
        self.ai_send_button.clicked.connect(self.ai_send)

        self.ai_history.setReadOnly(True)
        
        self.ai_chat_context = []

    def load_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_name:

            with open(file_name, 'r', encoding='utf-8') as file:
                text = file.read()
                self.main_text.setPlainText(text)

    def ai_send(self): 
        request = f"[👤] {self.ai_request.toPlainText()}" 
        self.ai_chat_context.append(request) 
        self.ai_history.setPlainText('\n'.join(self.ai_chat_context)) 
        self.ai_request.setPlainText('') 
        
        cursor = QtGui.QTextCursor(self.ai_history.document())
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
        self.ai_history.setTextCursor(cursor)
        self.ai_history.ensureCursorVisible()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
