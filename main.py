import sys
from PyQt6.QtWidgets import QApplication
from src.app.aieditor import Aieditor


def main():
    app = QApplication(sys.argv)
    window = Aieditor()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
