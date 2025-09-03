from PySide6.QtWidgets import QMainWindow, QMenu, QMenuBar

from app.core.navigation import Navigation
from app.scan.scan_view import ScanView


class MainView(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(1000, 800)
        self._set_up_menu()

        self.scan_view = ScanView()

        # It's the responsibility of the controller to add the pages to the navigation
        # after links between views and models are set up.
        self.navigation = Navigation()
        self.setCentralWidget(self.navigation)

    def _set_up_menu(self) -> None:
        file_menu = QMenu("&File", self)
        file_menu.addAction("E&xit", self.close)

        menu_bar = QMenuBar()
        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)
