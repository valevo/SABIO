import pandas as pd

from src.engines import rand_engine

static_field_descriptions = {
    "object_keywords": 'enter keyword', 
    "object_start_date": 'enter start date',
    "object_end_date": 'enter end date'
}


class Dataset:
    def __init__(self, data, id_, name, source_url, params, available_engines):
        self.name = name
        self.id = id_
        self.source_url = source_url
        
        self.static_params = ["object_keywords", 
                              "object_start_date",
                              "object_end_date"]
        
        self.params = {p.label:p for p in params}
        
        self.available_engines = tuple(available_engines)
        
        self.data = data

        self.objectIDs = list(data.ObjectID)
        
    def object_count(self):
        return self.data.shape[0]

    def __len__(self):
        return self.object_count()


    # def __lt__(self, other):
    #    if not isinstance(other, Dataset):
    #        raise ValueError
    #    return self.id < other.id
    
    def get_object(self, objectID):
        obj = self.data[self.data.ObjectID == objectID]
        return {
            "id": int(obj.ObjectID),
            "name": obj.Title.item(),
            "description": obj.Description.item(),
            "thumbnail_url": None,
            "image_url": None,
            "source_url": None,
            "attributes": {} # list of strings, addititional attributes
        }
    
    
    def to_dict(self):
        return {
            "id": self.id,  # Dataset ID
            "name": self.name,  # Dataset name
            "source_url": self.source_url,
            "object_count": self.object_count(),
            "static_field_descriptions": static_field_descriptions,
            "params": [p.to_dict() for p in sorted(self.params.values())],
            "available_engines": [e.id for e in self.available_engines]
        }    

    
class DatasetParam:
    def __init__(self, id_, label, description, control, options):
        self.id = id_
        self.label = label
        self.description = description
        if not control in ("select", "autocomplete"):
            raise ValueError("Argument `control` must be one of {select, autocomplete}")  
        self.control = control
        self.options = options # options only required for select, not for autocomplete
    
    def __eq__(self, other):
        if not other.__class__ == self.__class__:
            return False
        return self.id == other.id and self.label == other.label and self.control == other.control # and self.options == other.options
    
    def __hash__(self):
        return hash((self.id, self.label, self.control)) # self.options
    
    
    def autocomplete(self, dataset, column, keyword):
        strings = dataset[column]
        return sorted({s for s in strings 
                       if isinstance(s, str) and s.startswith(keyword)})
    
    
    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "description": self.description,
            "control": self.control,
            "options": self.options
        }
  


        
nmvw_path = "NMvW_data/Objects_1000000.csv.gz"
nmvw_obj_tbl = pd.read_csv(nmvw_path, low_memory=False)

ObjectName = DatasetParam(0, "ObjectName", "The type of object, e.g. foto.", 
                      control="autocomplete", options={})

NMvW_params = (ObjectName,)

NMvW = Dataset(nmvw_obj_tbl, id_="NMvW Dataset v0, 
               name="Part of the collection of the Nationaal Museum van Wereldculturen", 
               source_url="https://collectie.wereldculturen.nl", 
               params=NMvW_params,
               available_engines=(rand_engine,))
               
