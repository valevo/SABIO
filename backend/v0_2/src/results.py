import pandas as pd

attributes = ["BeginISODate", "EndISODate"] # + [p.label for p in NMvW_params]

class Result:
    def __init__(self, param_names, rows, scores, 
                 score_details, min_score, max_score):
        self.attributes = attributes + param_names 

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
        rng = range(self.values.shape[0]) if (n<0) else range(n)
        for i in rng:
            obj_dict = {
                "id": self.ids[i],
                "name": self.titles.iloc[i],
                "thumbnail_url": self.thumbnails.iloc[i],
                "values": list(map(lambda x: x if isinstance(x, str) else str(x), #x.item(), 
                                   self.values.iloc[i])),
                "x": list(map(float, self.x.iloc[i])),
                
                "score": self.scores.iloc[i].item(),
                "score_details": self.score_details.iloc[i]
            }
            
            yield obj_dict
        
        
    def to_dict(self):
        return {
            "attributes": self.attributes,
            "results": list(self.iter_objects())
        }