# A SaveModel is what constitutes one "Savegame Unit",
# e.g. A SNES emulator can work with a Savestate (one raw data file, one screenshot) or a Battery save (only a raw data file)

class SaveUnit:
    def __init__(self, name, pairs = {}):
        self.name = name
        self.pairs = pairs # Key = name (e.g. 'savestate file'); Value = file extension

class NewVegasSave(SaveUnit):
    def __init__(self):
        super().__init__("Fallout New Vegas", {'raw data' : 'fos', 'backup' : '.fos.bak'})