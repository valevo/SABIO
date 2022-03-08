from src.engines.engines import Engine

class ContentLengthEngine(Engine):
    
    # max_len of 1000 leads to 7.5% of the data being removed
    def __init__(self, max_len=1000, cached=True, **engine_params):
        super().__init__(**engine_params)
        self.min_score = 0. # np.random.random()*100
        self.max_score = 1.
        self.max_len = max_len 
        
        if cached:
            self.cached = False
            self.scores_cached, self.details_cached = self.score_and_detail(self.dataset.data)
            self.cached = True
        else:
            self.cached = False
                                                        
    def char_text_length(self, obj):
        return len(obj.Title) + len(obj.Description)
        
        
    def score_and_detail(self, objects, **param_dict):
        if self.cached:
            ids = objects.index
            return self.scores_cached.loc[ids], self.details_cached.loc[ids]
        
        lengths = objects.fillna("").progress_apply(self.char_text_length, 
                                                    axis="columns")
        # this will lead objects with length > self.max_len
        # to have a score > 1.0 and hence be removed from the result set
        lengths = lengths/self.max_len
        lengths.name = "score"
        
        details = objects.Title.apply(lambda x: dict())
        details.name = "score_details"
        
        return lengths, details
        
