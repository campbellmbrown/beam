from PySide6.QtWidgets import QMainWindow, QMenu, QMenuBar, QVBoxLayout, QWidget


class MainView(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(1000, 800)

        file_menu = QMenu("&File", self)

        file_menu.addAction("E&xit", self.close)

        menu_bar = QMenuBar()
        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)

        layout = QVBoxLayout()
        # Add content here

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
