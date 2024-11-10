import sys
from PyQt6 import QtWidgets
from src.app.aieditor import Aieditor


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Aieditor()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
