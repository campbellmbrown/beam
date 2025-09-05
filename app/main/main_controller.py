from app.main.main_model import MainModel
from app.main.main_view import MainView
from app.scan.scan_controller import ScanController


class MainController:
    def __init__(self, view: MainView, model: MainModel) -> None:
        self.view = view
        self.model = model

        self.scan_controller = ScanController(view.scan_view, model.scan_model)

        view.navigation.add_page(view.scan_view, "Scan")
