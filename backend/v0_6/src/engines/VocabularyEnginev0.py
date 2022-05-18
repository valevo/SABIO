import numpy as np
import pandas as pd

from src.engines.engines import Engine, EngineParam

import re
import json

from collections import Counter

class VocabularyEngine(Engine):
    def __init__(self, **engine_args):
        super().__init__(**engine_args)
        self.min_score = 0. # np.random.random()*100
        self.max_score = 1.
        self.vocab_parser = re.compile("\s*,\s*")

        with open("src/engines/vocabulary_presets.json") as handle:
            self.vocab_examples = json.load(handle)
            self.all_examples = self.vocab2re(",".join(self.vocab_examples.values()))
            self.vocab_examples = {list_name: self.vocab2re(word_list)
                                   for list_name, word_list in self.vocab_examples.items()}

        # constanct scores and details make no sense for this engine!
        # yes they do - these are the scores for the example list
        # -> this will allow the /examples route to compute faster
        self.constant_scores, self.constant_details = self.score_and_detail(self.dataset.data)
        

    # assumes that `raw_vocab` is a string of comma-separated terms
    def vocab2re(self, raw_vocab):
        v_ls = self.vocab_parser.split(raw_vocab.strip())
        return re.compile("|".join(rf"\b{w}\b" for w in v_ls))
    
    # assumes that vocab_re = "\bword1\b|\bword2\b|..."
    def re2vocab(self, vocab_re):
        return vocab_re.pattern.replace("|", ",").replace(r"\b", "")
        
        
#     def score(self, objects, round_to=3, **param_dict):
#         if "vocabulary" in param_dict:
#              vocab_re = self.vocab2re(param_dict["vocabulary"])
#         else:
#              vocab_re = self.all_examples

#         scores = objects[["Title", "Description"]].fillna("").apply(
#                          lambda r: len([w for txt in row
#                                         for w in vocab_re.findall(txt)]),
#                          axis=1
#              )
        
#         scores.name = "score"
        
#         return scores

    def score(self, objects, round_to=3, **param_dict):
        raise NotImplementedError("VocabularyEngine doesn't support scoring without details!")
    
    
    def score_details(self, objects, round_to=3, **param_dict):
        raise NotImplementedError("VocabularyEngine doesn't support details without scoring!")
        
        
    def score_and_detail(self, objects, round_to=3, **param_dict):
        if ("constant_scores" in param_dict) and (param_dict["constant_scores"] is True):
            return self.constant_scores, self.constant_details
        
        if "vocabulary" in param_dict and param_dict["vocabulary"].strip():
             vocab_re = self.vocab2re(param_dict["vocabulary"])
        else:
             vocab_re = self.all_examples

        def process_obj(txt):
            counts = Counter([w for w in vocab_re.findall(txt)])
            score = sum(counts.values())
            percents = {w: (c/score).round(round_to) for w, c in counts.items()}

            return percents, score

        tups = objects.Texts.fillna("").apply(process_obj, axis=1)
        
        scores = tups.apply(lambda t: t[1])
        scores = (scores/scores.max()).round(round_to)
        scores.name = "score"
        
        details = tups.apply(lambda t: t[0])
        details.name = "score_details"
        
        return scores, details
    
    
    
    
#     def score_and_detail(self, objects, round_to=3, **param_dict):
#         if "vocabulary" in param_dict and param_dict["vocabulary"].strip():
#              vocab_re = self.vocab2re(param_dict["vocabulary"])
#         else:
#              vocab_re = self.all_examples

                
        
#         text_fields = ["Title", "Description"]
        
#         relevant = objects[].fillna("")

