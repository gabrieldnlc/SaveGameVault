from PySide6.QtWidgets import *
from PySide6.QtCore import QStringListModel, QModelIndex

class GameList(QListView):
    def __init__(self):
        super().__init__()

    def on_clicked(self, index : QModelIndex):
        print(f"selected: {self.model().data(index)}")

class UI_List():
    def __init__(self, games : dict):

        app = QApplication([])
        model = QStringListModel(games.keys())
        view = GameList()
        view.setModel(model)
        view.clicked.connect(view.on_clicked)

        view2 = QListView()
        view2.setModel(model)
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(view)
        layout.addWidget(view2)

        container.show()

        container.setWindowTitle("testing")
        app.exec()

if __name__ == "__main__":
    games = {"Fallout" : ["save1", "save2"], "KOTOR" : ["save 1"], "Persona" : ["save1, save2, save3"]}

    UI_List(games)
