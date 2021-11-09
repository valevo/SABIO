import numpy as np


class ResultObject:
    def __init__(self, id_, name, thumbnail_url, values, x, score, score_details):
        self.id = id_
        self.name = name
        self.thumbnail_url = thumbnail_url
        self.values = values
        self.x = x
        self.score = score
        self.score_details = score_details
        
        
from datasets import NMvW

from engines import rand_engine

        
def search_by_date(start, end, engine, min_score, max_score):
    NotImplemented
    
    

    
    
    
class Search:
    
    def __init__(self):
        pass
    
    
    def search_by_keyword(self, kw, engine, min_score, max_score):
        relevant_fields = "ObjectName", "Title", "Description", "Provenance"
        bools = [[(kw in s.lower()) if isinstance(s, str) else False 
                     for s in NMvW.data[f]] for f in relevant_fields] 

        does_contain = np.sum(list((zip(*bools))), axis=1).astype("bool")
        print(does_contain.sum())
        result_rows = NMvW.data[does_contain]

        return result_rows
    
    
    
    def to_dict(self, row):
        values = self.get_values(row)
        return {
            "id": row.ObjectID.item(),
            "name": row.Title.item(),
            "thumbnail_url": None,
            "values": values,
            
    
    
    
    
        