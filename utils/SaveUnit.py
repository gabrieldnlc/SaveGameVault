# A SaveModel is what constitutes one "Savegame Unit",
# e.g. A SNES emulator can work with a Savestate (one raw data file, one screenshot) or a Battery save (only a raw data file)

class SaveUnit:
    def __init__(self):
        self.pairs = {} # Key : Value -> name (e.g. 'savestate file') : file extension

        