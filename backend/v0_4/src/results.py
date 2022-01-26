import pandas as pd

attributes = ["BeginISODate", "EndISODate"] # + [p.label for p in NMvW_params]

class Result:
    def __init__(self, param_names, rows, scores, 
                 score_details, min_score, max_score):
        self.attributes = attributes + param_names 
        
#         self.ids = rows.index.astype("string")
        titles = rows.Title.fillna("").astype("string")
        thumbnails = pd.Series([""]*rows.shape[0],
                                   name="Thumbnail",
                                   index=rows.index).astype("string")
        
        
        # the actual values
        values = rows[self.attributes].astype(str)
        
#         values = values.apply(lambda x: x if isinstance(x, str) else str(x))
        
        # x-locations as values in [0,1]
        xs = values.apply(self.values_to_x, axis=0)
        xs.columns = ["x_"+c for c in xs.columns]
        
#         scores = scores
#         score_details = score_details
        self.min_score = min_score
        self.max_score = max_score
        
        self.df = pd.concat([titles, thumbnails, values, xs, scores, score_details], axis=1)
        
        

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
    
        
    def iter_objects(self):
        for i, record in self.df.to_dict("index").items():
            obj_dict = {
                "id": str(i),
                "name": record["Title"],
                "thumbnail_url": record["Thumbnail"],
                
                "values": [record[attr] for attr in self.attributes],
                "x": [record["x_"+attr] for attr in self.attributes],
                
                "score": float(round(record["score"], 3)),
                "score_details": record["score_details"]
            }
            
            yield obj_dict
            
            
    def to_dict(self):
        return {
            "attributes": self.attributes,
            "results": list(self.iter_objects())
        }
        
    
    
