import pandas as pd



class Dataset:
    def __init__(self, dataframe, id_, name, source_url, params, available_engines):
        self.name = name
        self.id = id_
        self.source_url = source_url
        
        

        
class DatasetParam:
    def __init__(self, id_, label, description, control="autocomplete", options=None)
    
    
    
    
        if control == "select" and options is None:
            raise ValueError("control=select but no options given!")