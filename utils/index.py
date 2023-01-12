# reminder: set the remove_bom parameter in GetContentString()
import json

class Index:
    def __init__(self, folders = {}):
        self.folders = folders # Key = folder; Value = a SaveUnit model
    
    
