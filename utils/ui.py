from PySide6.QtWidgets import *
from PySide6.QtCore import QStringListModel


class UI_List():
    def __init__(self, games : list[str]):
        app = QApplication([])
        model = QStringListModel(games)
        view = QListView()
        view.setModel(model)
        view.show()
        app.exec()

