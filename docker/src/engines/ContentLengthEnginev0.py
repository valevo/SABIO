import numpy as np
import pandas as pd
from engines.Engine import Engine, EngineParam, CachedEngine



class ContentLengthEngine(CachedEngine):
    def __init__(self, ID, name, params, cache_dir, max_len=None):
        super().__init__(ID, name, params, cache_dir)
        self.min_score = 0.
        self.max_score = 1.
        self.max_len = max_len
        
        
    def char_text_length(self,txt):
        return len(txt)
    
    def word_text_length(self, txt):
        return len(txt.split())
    
    def get_longest_words(self, words, normalise_len=True, round_to=3):
        len_sorted = sorted(set(words), key=lambda w: len(w), reverse=True)
        
        total_len = sum(map(len, words))#self.char_text_length(txt)
        if normalise_len:
            return {w: round(len(w)/total_len, 3) for w in len_sorted[:5]}
        else:
            return {w: len(w) for w in len_sorted[:5]}

    def eighty_percent_max_len(self, dataset, q=0.8):
        lens = dataset.data.Texts.progress_apply(self.char_text_length)
        return np.quantile(lens, q)
        
        
    def _score_and_detail(self, dataset, indices=None, round_to=3, **params):
        max_len = self.max_len or self.eighty_percent_max_len(dataset)
        
        lengths = dataset.data.Texts.progress_apply(self.char_text_length)
        # this will lead objects with length > self.max_len\
        # to have a score > 1.0 and hence be removed from the result set
        lengths = (lengths/max_len).round(round_to)
        lengths.name = "score"
        
        get_longest_words = lambda words: self.get_longest_words(words, round_to=round_to)
        details = dataset.tokenise().progress_apply(get_longest_words)
        details.name = "score_details"
        
        return lengths, details
