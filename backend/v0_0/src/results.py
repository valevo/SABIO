class Searcher:
    def __init__(self, dataset, engines):
        self.dataset = dataset
        self.engines = engines
        
        
    def submit(self, **params):
        kw_results = self.match_keyword(self.dataset, **params)
        date_results = self.match_date(self.dataset, **params)
        extra_param_results = self.match_extra_params(self.dataset, **params)
        
        # filter here, then pass to engine for scoring
        
        cur_engine = self.engines[params["engine_id"]]
        engine_params = {k:v for k,v in params.items()
                         if k.startswith("engine_param_")}
        engine_scores = cur_engine.score(self.dataset)
        
        # filter by engine_min_score, engine_max_score
        
        # return what is left as a SearchResult object
        # has:

        
    def match_keyword(self, dataset, object_keywords, **unused_args):
        pass
    
    def match_date(self, dataset, object_start_date, object_end_date, **unused_args):
        pass
    
    
    def match_extra_params(self, dataset, **params):
        extra_params = {k:v for k,v in params.items() 
                        if k.startsiwth("object_param_")}
        pass
    
    def use_vocabulary_items(self):
        pass # what about recomputation 
        
class SearchResult:
    def __init__(self):
        pass
    
    def to_dict(self):
            # atributes?
            # results:
                # id
                # name
                # thumbnail_url -> why
                # x (= scores)
                # score ? (= overall score of result?)
                # score_details (= ...)
        pass
        
        
        
# all search parameters act as filters on Dataset.data
# -> perhaps: let matching return indexes (or boolean list), then intersect 
        
# let Dataset specify:

# - which columns are relevant for keyword matching
# - which additional search parameters exist (match by ID)


# let DatasetParam specify:

# - how search is done (static method)


# let Engine specify:

# - how extra engine params are used 
# -> what about recomputation of engine ?