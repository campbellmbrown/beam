from app.main.main_view import MainView
from app.scan.scan_controller import ScanController


class MainController:
    def __init__(self, view: MainView) -> None:
        self.view = view

        self.scan_controller = ScanController(view.scan_view)

        view.navigation.add_page(view.scan_view, "Scan")
