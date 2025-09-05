import sys

from PySide6.QtWidgets import QApplication

from app.dialogs.exception_view import ExceptionView
from app.main.main_controller import MainController
from app.main.main_model import MainModel
from app.main.main_view import MainView

if __name__ == "__main__":
    sys.excepthook = ExceptionView.show_exception_dialog
    app = QApplication(sys.argv)

    main_view = MainView()
    main_model = MainModel()
    main_controller = MainController(main_view, main_model)

    main_view.show()
    sys.exit(app.exec())
