import numpy as np
import pandas as pd

from tqdm import tqdm
tqdm.pandas()

from src.engines.Engine import Engine

import re
import json

from collections import Counter

print("IMPORTING VOCABENGINE")

class VocabularyEngine(Engine):
    def __init__(self, ID, name, params):

        super().__init__(ID, name, params)
        self.min_score = 0.
        self.max_score = 1.
        self.vocab_parser = re.compile("\s*,\s*")
        
        with open("src/engines/vocabulary_presets.json") as handle:
            self.vocab_examples = json.load(handle)
            self.all_examples = self.vocab2re(",".join(self.vocab_examples.values()))
            self.vocab_examples = {list_name: self.vocab2re(word_list)
                                   for list_name, word_list in self.vocab_examples.items()}

        
    # assumes that `raw_vocab` is a string of comma-separated terms
    def vocab2re(self, raw_vocab):
        v_ls = self.vocab_parser.split(raw_vocab.strip())
        return re.compile("|".join(rf"\b{w}\b" for w in v_ls))
    
    # assumes that vocab_re = "\bword1\b|\bword2\b|..."
    def re2vocab(self, vocab_re):
        return vocab_re.pattern.replace("|", ",").replace(r"\b", "")

    
    def score_and_detail(self, dataset, indices, round_to=3, **params):
#         params = self.prep_engine_params(params)
        
#         if ("constant_scores" in param_dict) and (param_dict["constant_scores"] is True):
#             return self.constant_scores, self.constant_details
        if "vocabulary" in params and params["vocabulary"].strip():
             vocab_re = self.vocab2re(params["vocabulary"])
        else:
             vocab_re = self.all_examples

        def process_obj(txt):
            counts = Counter([w for w in vocab_re.findall(txt)])
            score = sum(counts.values())
            percents = {w: round(c/score, round_to) for w, c in counts.items()}
            return percents, score

        cur_texts = dataset.data.Texts.loc[indices]
        
        tups = cur_texts.progress_apply(process_obj) # description=f"{self} on {dataset}"
        
        scores = tups.apply(lambda t: t[1])
        scores = (scores/scores.max()).round(round_to)
        scores.name = "score"
        
        details = tups.apply(lambda t: t[0])
        details.name = "score_details"
        
        return scores, details
    
    
    
    # to make this a cached engine:
#     def is_cached(self, dataset, **params):
#         if "vocabulary" in params or params["vocabulary"].strip():
#             return True
#         # this engine is only cached if no vocabulary is given 
#         return False
            
        
        
        
