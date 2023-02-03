import jsons

class SaveUnit:
    """A SaveModel is what constitutes one "Savegame Unit",
       e.g. A SNES emulator can load a Savestate (one raw data file, one screenshot) or a Battery save (only a raw data file)."""
    def __init__(self, name, files = {}):
        self.name = name
        self.files = files
        """Key = name (e.g. 'savestate file'); Value = file extension"""

class NewVegasSave(SaveUnit):
    """Test class"""
    
    def __init__(self):
        super().__init__("Fallout New Vegas", {'raw data' : 'fos', 'backup' : '.fos.bak', 'nvse file (modding)' : '.nvse'})

def unit_to_json(unit : SaveUnit) -> str:
    return jsons.dumps(unit)

def json_to_unit(json : str, cls : type) -> SaveUnit:
    return jsons.loads(json, cls)
