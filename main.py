import sys
from PyQt6 import QtWidgets, uic
from PyQt6 import QtWidgets, QtGui
from src.ai_requests import AI


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        uic.loadUi('main.ui', self)

        self.open_file.clicked.connect(self.load_file)
        self.ai_send_button.clicked.connect(self.ai_send)

        self.ai_history.setReadOnly(True)
        self.selected_text = ""

        self.ai = AI()
        self.ai_mode = self.ai.SUMMARING
        
        self.ai_chat_context = []
        self.main_text.selectionChanged.connect(self.select_text)

    def select_text(self):
        self.selected_text = self.main_text.textCursor().selectedText()

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

    def ai_analysis(self):
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

    def add_to_history(self, *texts):
        for text in texts:
            self.ai_chat_context.append(text)
        self.ai_history.setPlainText('\n'.join(self.ai_chat_context))

    def move_cursor_down(self, t):
        cursor = QtGui.QTextCursor(t.document())
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.End)
        t.setTextCursor(cursor)

    def ai_send(self): 

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
