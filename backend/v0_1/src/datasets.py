import pandas as pd
import numpy as np

from functools import reduce


# from src.engines import rand_engine


static_field_descriptions = {
    "object_keywords": 'enter keyword', 
    "object_start_date": 'enter start date',
    "object_end_date": 'enter end date'
}



# TODO: cast categorical columns to categorical data type? 
# => makes search in pd.DataFrame faster


class Dataset:
    def __init__(self, dataframe, id_, name, source_url, params, available_engines=[]):
        self.id = id_
        self.name = name
        self.source_url = source_url
        
        self.min_date = dataframe.BeginISODate.min()
        self.max_date = dataframe.EndISODate.max()
        self.object_count = dataframe.shape[0]
        
        self.params = {p.id: p for p in params}
        self.available_engines = {e.id: e for e in available_engines}
        
        self.data = dataframe
        
        text_search_fields = ["Title", "ObjectName", "Description"]
        self.search_texts = self.data[text_search_fields].fillna("").apply(lambda row: " ".join(row).lower(), axis=1)
        
        
    def add_engine(self, engine):
        self.available_engines.update(
            {engine.id: engine}
        )
                      
    def to_dict(self):
        return {
            "id": self.id,  # Dataset ID
            "name": self.name,  # Dataset name
            "source_url": self.source_url,
            "object_count": self.object_count,
            "min_date": int(self.min_date),
            "max_date": int(self.max_date),
            "static_field_descriptions": static_field_descriptions,
            "params": [p.to_dict() for i, p in sorted(self.params.items())],
            "available_engines": [e.id for i, e in sorted(self.available_engines.items())]
        }
    
    
    def __hash__(self):
        return hash((self.id, self.name, self.source_url,
                     self.min_date, self.max_date, self.object_count,
                    tuple(self.params.keys()), 
                    tuple(self.available_engines.keys())
                    ))
    
    def get_obj(self, obj_id):
        return self.data.loc[obj_id]
    
    
    def search(self, kws, start_date, end_date, **obj_params):
        match_kw = self.search_by_keywords(kws)#.astype("bool")
        match_date = self.search_by_date(start_date, end_date)#.astype("bool")
        
        param_matches = {p_id: self.params[p_id].search(self.data, val) for p_id, val in obj_params.items()}
        
        param_matches = reduce(lambda a,b: a & b, param_matches.values())
        
        return self.data[match_kw & match_date & param_matches]
        

    def search_by_keywords(self, kws, return_bool_series=True):      
        prep_kws = "|".join(kws.lower().replace(", ", ",").split(","))
        
        if (not kws.strip()) or (not prep_kws):
            does_contain = [True]*self.object_count
        else:
            print("SUBMITTED KEYWORD: ", prep_kws)
            does_contain = self.search_texts.str.contains(prep_kws, regex=False)
        
        if return_bool_series: return does_contain
        return self.data[does_contain]
    
    
    def search_by_date(self, start_date, end_date, return_bool_series=True):
        from datetime import datetime
        frmt = "%Y-%m-%d"
        try:
            start_year, end_year = datetime.strptime(start_date, frmt), datetime.strptime(end_date, frmt)
        except ValueError:
            start_year, end_year = self.min_date, self.max_date
        
#         start_year = int(start_date.split("-")[-1])
#         end_year = int(end_date.split("-")[-1])
        
        in_range = (self.data.BeginISODate >= start_year) &\
                    (self.data.EndISODate <= end_year)
        
        if return_bool_series: return in_range
        
        return self.data[in_range]
    
    
    def detail_object(self, obj_id):
        obj = self.data.loc[int(obj_id)]
        
        return {
            "id": str(obj_id),
            "name": obj.Title if isinstance(obj.Title, str) else "",
            "description": obj.Description if isinstance(obj.Description, str) else "",
            "thumbnail_url": "",
            "image_url": "",
            "source_url": f"https://hdl.handle.net/20.500.11840/{obj_id}",
            "attributes": {
                "dated": str(obj.Dated)
            }
        }
                
        

        
class DatasetParam:
    def __init__(self, id_, label=None, description="", control="autocomplete", options=None):
        if control == "select" and options is None:
            raise ValueError("control=select but no options given!")
            
        self.id = id_
        self.label = id_ if (label is None) else label
        self.description = description
        self.control = control
        self.options = options
        
        
    def autocomplete(self, df, kw):
        possibilities = sorted(df[self.id].unique())
        
        if kw == "": # if not kw
            return possibilities
        
        return [x for x in possibilities if x.lower().startswith(kw.lower())]
    
    
    def search(self, data, option, return_bool_series=True):
        if option == "":
            is_option = pd.Series([True]*data.shape[0])
        else:
            is_option = data[self.id] == option
        
        if return_bool_series:
            return is_option
        
        return data[is_option]
    
    
        
    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "description": self.description,
            "control": self.control,
            "options": self.options
        }

    def __eq__(self, other):
        if not other.__class__ == self.__class__:
            return False
        return self.id == other.id and self.label == other.label and self.control == other.control # and self.options == other.options
    
    
    def __hash__(self):
        return hash((self.__class__, self.id, self.label, self.control)) # self.options
            
            
NMvW_params = [
    DatasetParam("Department", label=None,
                 description="Global region, e.g. 'Circumpolare Gebieden'"),
    
    DatasetParam("Classification", label=None,
                 description="Type of object, e.g. 'Audiovisuele collectie'")

]

        
        

df = pd.read_csv("NMvW_data/v0.csv.gz", 
                 dtype=dict(Provenance="string", RelatedWorks="string"))

# TODO: save & load DF s.t. these lines are not necessary here                
df["ObjectID"] = df.ObjectID.astype("int")
df = df.set_index("ObjectID")
                
        
# NMvW = Dataset(df, "NMvW_v0", 
#                "Nationaal Museum van Wereldculturen 1M",
#                "https://collectie.wereldculturen.nl/",
#                NMvW_params,
#                available_engines=[rand_engine])






attributes = ["BeginISODate", "EndISODate"] + [p.label for p in NMvW_params]

class Result:
    def __init__(self, rows, scores, score_details, min_score, max_score):
        self.attributes = attributes

        self.ids = rows.index.astype("string")
        self.titles = rows.Title.fillna("").astype("string")
        self.thumbnails = pd.Series([""]*rows.shape[0]).astype("string")
        
        
        # the actual values
        self.values = rows[attributes]
        
        # x-locations as values in [0,1]
        self.x = self.values.apply(self.values_to_x, axis=0)
        
        self.scores = scores
        self.score_details = score_details
        self.min_score = min_score
        self.max_score = max_score
    
    
    def values_to_x(self, col):
        if col.dtype == "int":
            return self.scale_num_var(col)
        elif col.dtype == "object" or col.dtype == "string":
            return self.transform_cat_var(col)
        else: 
            raise ValueError(f"Don't know how to transform columns of type `{col.dtype}` into an x-location!")
    
    
    def scale_num_var(self, col, round_to=3):
        if len(col.unique()) == 1: 
            return (col - col.min()).round(round_to)
     
        return ((col - col.min())/(col.max() - col.min())).round(round_to)
    
    
    def transform_cat_var(self, col, scale=True, round_to=3):
        labels = sorted(col.unique())
        num_labels = list(range(len(labels)))
        mapping = dict(zip(labels, num_labels))
        if scale: return self.scale_num_var(col.map(mapping), round_to=round_to)
        return col.map(mapping)
       

    # TODO: solution with `.iloc`, might have bad complexity
    def iter_objects(self, n=-1):
        rng = range(self.values.shape[0]) if (n==-1) else range(n)
        for i in rng:
            obj_dict = {
                "id": self.ids[i],
                "name": self.titles.iloc[i],
                "thumbnail_url": self.thumbnails.iloc[i],
                "values": list(map(lambda x: x if isinstance(x, str) else x.item(), 
                                   self.values.iloc[i])),
                "x": list(map(float, self.x.iloc[i])),
                
                "score": self.scores[i].item(),
                "score_details": self.score_details.iloc[i]
            }
            
            yield obj_dict
        
        
    def to_dict(self):
        return {
            "attributes": self.attributes,
            "results": list(self.iter_objects())
        }
                
            






#         bools = [
#             [(kw in s.lower()) if isinstance(s, str) else False 
#                      for s in self.data[f]] for f in relevant_fields] 
#         does_contain = np.sum(list((zip(*bools))), axis=1).astype("bool")
        
