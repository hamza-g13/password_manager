import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from PyQt5.QtWidgets import QApplication
from src.core.storage import storage
from src.gui.main_window import MainWindow
from src.gui.dialogs import LoginDialog


def main():
    app = QApplication(sys.argv)


    app.setStyle("Fusion")
    storage_manager = storage()
    login = LoginDialog(storage_manager)

    if login.exec_():
        window = MainWindow(storage_manager)
        window.show()

        sys.exit(app.exec_())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
