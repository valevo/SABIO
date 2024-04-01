from datetime import datetime

import pandas as pd
import numpy as np

from functools import reduce
import json
import re

from datetime import datetime as dt


static_field_descriptions = {
    "keywords": 'enter keyword',
    "start_date": 'enter start date',
    "end_date": 'enter end date'
}



# TODO: cast categorical columns to categorical data type? 
# => makes search in pd.DataFrame faster


class Dataset:
    parse_date = "%Y-%m-%d"
    format_date = "%04Y-%m-%d"
    
    @staticmethod
    def parse_dataset_meta(filename):
        with open(filename) as handle:
            meta = json.load(handle)
            
        params = [DatasetParam(p_id, **p_arg_dict) 
                  for p_id, p_arg_dict in meta["dataset_params"].items()]
        
        return meta, params
    
    @classmethod
    def with_dataset_meta(cls, dataframe, meta_filename, image_source, available_engines=[]):
        meta_dict, dataset_params = cls.parse_dataset_meta(meta_filename)
        instance = cls(dataframe, 
                       ID=meta_dict["id"], 
                       name=meta_dict["name"], 
                       dataset_url=meta_dict["dataset_url"], 
#                        object_base_url=meta_dict["object_base_url"],
                       text_columns=meta_dict["text_columns"],
                       params=dataset_params,
                       image_source=image_source,
                       available_engines=available_engines
                      )
        
        return instance

    def __init__(self, dataframe, ID, name, 
                 dataset_url,
                 text_columns,
                 params, image_source,
                 available_engines=[]):
        
        self.ID = ID
        self.name = name
        self.dataset_url = dataset_url
#         self.object_base_url = object_base_url

        self.min_date = dataframe.start_date.min()
        self.max_date = dataframe.end_date.max()
        
        self.object_count = dataframe.shape[0]
        
        self.params = {p.id: p for p in params}
        self.image_source = image_source
        self.available_engines = {e.ID: e for e in available_engines}
        
        self.data = dataframe
        self.index = self.data.index
        
#         text_search_fields = ["Title", "ObjectName", "Description"]

        self.text_columns = ["name", "description"] + text_columns
        self.data[self.text_columns] = self.data[self.text_columns].fillna("")
        self.data["Texts"] = self.data[self.text_columns].apply(lambda row: "\n".join(row).lower().strip(), axis=1)
#         self.texts = self.data[text_columns].apply(lambda row: " ".join(row).lower(), axis=1)



        self.kw_parser = re.compile("\s*,\s*")
        
        
    def add_engine(self, engine):
        self.available_engines.update({engine.ID: engine})
                      
    def to_dict(self):
        return {
            "id": self.ID,  # Dataset ID
            "name": self.name,  # Dataset name
            "source_url": self.dataset_url,
            "object_count": self.object_count,
            "min_date": self.min_date.strftime(self.format_date), # "0001-01-01",
            "max_date": self.max_date.strftime(self.format_date), # "2018-01-01",
            "static_field_descriptions": static_field_descriptions,
            "params": [p.to_dict() for i, p in sorted(self.params.items())],
            "available_engines": [e.ID for i, e in sorted(self.available_engines.items())]
        }
    
    
    def __hash__(self):
        return hash((self.id, self.name, self.dataset_url,
                     self.min_date, self.max_date, self.object_count,
                    tuple(self.params.keys()), 
                    tuple(self.available_engines.keys())
                    ))
    
    def __len__(self):
        return self.data.shape[0]
    
    def get_obj(self, obj_id):
        return self.data.loc[obj_id]
    
    def sample(self, **kwargs):
        return self.data.sample(**kwargs)
    
    
    def tokenise(self):
        # tokenisation should eventually be handled by a tokeniser that
        # belongs to the dataset (or that the dataset can reference)
        return self.data.Texts.str.split()
    
    def segment(self, level):
        if level == "paragraph":
            return self.data.Texts.str.split("\n")
#             return self.data.Texts.apply(lambda txt: txt.split("\n"))
#             return pd.Series([t.split("\n") for t in self.data.Texts], 
#                              name="Texts",
#                             index=self.index)
#             return pd.Series([p for t in self.data.Texts for p in t.split("\n")], name="Texts")
        else:
            raise NotImplementedError("Only paragraph segmentation (i.e. by \\n) implemented.")
    
    
    def search(self, kws, start_date, end_date, indices_only=True, **obj_params):
        match_kw = self.search_by_keywords(kws)#.astype("bool")
        match_date = self.search_by_date(start_date, end_date)#.astype("bool")
        
        param_matches = {p_id: self.params[p_id].search(self.data, val) for p_id, val in obj_params.items()}
        
        param_matches = reduce(lambda a,b: a & b, param_matches.values())
        
        search_matches = match_kw & match_date & param_matches
        
        if indices_only:
            return self.index[search_matches]
        else:
            return self.data[search_matches]
        

    def search_by_keywords(self, kws, return_bool_series=True):     
#         prep_kws = "|".join(kws.lower().replace(", ", ",").split(","))
        #TODO: make more robust against whitespaces & other errors
        prep_kws = "|".join(self.kw_parser.split(kws.lower()))
        
        if (not kws.strip()) or (not prep_kws):
            # does_contain = pd.Series([True]*self.object_count)
            does_contain = self.data.Texts.str.contains("", regex=False)
        else:
            print("SUBMITTED KEYWORDS: ", prep_kws)
            does_contain = self.data.Texts.str.contains(prep_kws, case=False, regex=True)
        
        if return_bool_series: return does_contain
        return self.data[does_contain]
    
    
    def search_by_date(self, start_date, end_date, return_bool_series=True):
        try:
            start_year = datetime.strptime(start_date, self.parse_date).date()
            end_year = datetime.strptime(end_date, self.parse_date).date()
            #start_year, end_year = start_year.year, end_year.year
        except ValueError:
            start_year, end_year = self.min_date, self.max_date
        
        
        in_range = (self.data.start_date >= start_year) &\
                    (self.data.end_date <= end_year)
        
        if return_bool_series: return in_range
        
        return self.data[in_range]
    
    
    def detail_object(self, obj_id):
        obj = self.data.loc[obj_id]
        
        return {
            "id": str(obj_id),
            "name": obj["name"], # if isinstance(obj.name, str) else "",
            "description": obj.description, #if isinstance(obj.description, str) else "",
            "thumbnail_url": self.image_source.get_thumb(obj.name),
            "image_url": self.image_source.get_img(obj.name),
            "source_url": obj.source_url,
            "attributes": { # NEED TO BE MADE DYNAMIC
                "dated": str(obj.date_string)
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
        
        return [x for x in possibilities if kw.lower() in x.lower()]
#         return [x for x in possibilities if x.lower().startswith(kw.lower())]
    
    
    def search(self, data, option, return_bool_series=True):
        if option == "":
            is_option = pd.Series([True]*data.shape[0])
            is_option.index = data.index
        else:
            is_option = (data[self.id] == option)
        
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
            

        
        
class ImageSource:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path).fillna("")
        self.df["ID"] = self.df.ID.astype("int")
        self.df = self.df.set_index("ID")

        
    def get_img(self, object_ids):
        return self.get(object_ids, "img_URL")
    
    def get_thumb(self, object_ids):
        return self.get(object_ids, "thumbnail_URL")
    
    def get(self, object_ids, column):
        r = self.df.loc[object_ids]
        return r[column]

    
# # NMvW
      
# ## Load DataFrame
# df = pd.read_csv("../data/NMvW.v0_4.csv.gz", 
#                  dtype=dict(Provenance="string", RelatedWorks="string"))
# ## TODO: save & load DF s.t. these lines are not necessary here                
# # df["ID"] = df.ID.astype("int")
# df = df.set_index("ID")
# df["name"] = df["name"].fillna("")
# df["start_date"] = df.start_date.apply(lambda s: dt.strptime(s, Dataset.parse_date).date())
# df["end_date"] = df.end_date.apply(lambda s: dt.strptime(s, Dataset.parse_date).date())
# ## get Image Source
# images_NMvW = ImageSource("../data/NMvW.image_URLs.csv.gz")
# ## Instantiate Dataset object
# NMvW = Dataset.with_dataset_meta(
#                 df, "../data/NMvW.META.json", images_NMvW, available_engines=[])



# NMvW - V1
      
## Load DataFrame
df = pd.read_csv("../data/NMVW.v1_0.csv.gz", 
                 dtype=dict(Provenance="string",
                            Notes="string",
                            CuratorialRemarks="string"))
## TODO: save & load DF s.t. these lines are not necessary here                
# df["ID"] = df.ID.astype("int")
df = df.set_index("ID")
# df["name"] = df["name"].fillna("")
df = df.fillna("")
df["start_date"] = df.start_date.apply(lambda s: dt.strptime(s, Dataset.parse_date).date())
df["end_date"] = df.end_date.apply(lambda s: dt.strptime(s, Dataset.parse_date).date())
## get Image Source
images_NMvW = ImageSource("../data/NMVW.v1_0.image_URLs.csv.gz")
## Instantiate Dataset object
NMvW = Dataset.with_dataset_meta(
                df, "../data/NMVW.v1_0.META.json", 
                images_NMvW, available_engines=[])

# OpenBeelden

df = pd.read_csv("../data/OpenBeelden.v0_0.csv.gz").set_index("ID")
df["name"] = df["name"].fillna("")
df["start_date"] = df.start_date.apply(lambda s: dt.strptime(s, Dataset.parse_date).date())
df["end_date"] = df.end_date.apply(lambda s: dt.strptime(s, Dataset.parse_date).date())

images_OB = ImageSource("../data/OpenBeelden.image_URLs.csv.gz")
OpenBeelden = Dataset.with_dataset_meta(
                df, "../data/OpenBeelden.META.json", images_OB, available_engines=[])





















### OLD




### Define Parameters
# NMvW_params = [
#     DatasetParam("Department", label=None,
#                  description="Global region, e.g. 'Circumpolare Gebieden'"),
    
#     DatasetParam("Classification", label=None,
#                  description="Type of object, e.g. 'Audiovisuele collectie'")
# ]
### Instantiate Dataset object
# NMvW = Dataset(df, "NMvW_v0", 
#                "Nationaal Museum van Wereldculturen 1M",
#                "https://collectie.wereldculturen.nl/",
#                NMvW_params,
#                images,
#                available_engines=[])






# Datasets dictionary -> imported by app.py

                
            






#         bools = [
#             [(kw in s.lower()) if isinstance(s, str) else False 
#                      for s in self.data[f]] for f in relevant_fields] 
#         does_contain = np.sum(list((zip(*bools))), axis=1).astype("bool")
        
