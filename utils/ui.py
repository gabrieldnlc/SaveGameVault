from PySide6.QtWidgets import *
from PySide6.QtCore import QStringListModel, QModelIndex, Slot

class GameSavePairs():

    class SaveList(QListView):
        def __init__(self):
            super().__init__()

    class GameList(QListView):
        def __init__(self, parent_pair):
            super().__init__()
            self.parent_pair = parent_pair
            self.clicked.connect(self.updateSaveView)

        def setSibling(self, sibling : QListView):
            self.sibling = sibling

        @Slot(str)
        def updateSaveView(self, index : QModelIndex):
            selected_key = self.model().data(index)
            if (self.sibling != False):
                games = self.parent_pair.games
                saves = games[selected_key]
                self.sibling.setModel(QStringListModel(saves))
                self.sibling.setEnabled(len(saves) >= 1)
            


    

    def __init__(self, games : dict):

        self.games = games

        app = QApplication([])
        self.games_view = self.GameList(self)
        self.games_view.setModel(QStringListModel(self.games.keys()))
        
        self.saves_view = self.SaveList()
        self.saves_view.setEnabled(False)
        self.games_view.setSibling(self.saves_view)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.addWidget(self.games_view)
        layout.addWidget(self.saves_view)     

        container.show()
        container.setWindowTitle("testing")
        app.exec()
    
    


  

if __name__ == "__main__":
    games = {"Fallout" : ["save1", "save2"], "KOTOR" : ["save 1"], "Persona" : ["save1", "save2", "save3"], "Fallout 2" : []}
    
    GameSavePairs(games)
    
