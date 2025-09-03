from PySide6.QtWidgets import QTabWidget, QWidget


class Navigation(QTabWidget):
    """Extension of a QTabWidget to manage page navigation."""

    def __init__(self) -> None:
        super().__init__()
        self.setMovable(True)
        self.setDocumentMode(True)
        self.pages: list[QWidget] = []

    def add_page(self, page: QWidget, title: str) -> None:
        self.pages.append(page)
        self.addTab(page, title)
