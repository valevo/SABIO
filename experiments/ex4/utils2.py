import numpy as np
import scipy

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer



class Ngram:
    def __repr__(self):
        return (f"{self.ngram_range}-grams")
    
    
    
    def __init__(self, ngram_range=None, documents=None, precompute_freqs=False, term_doc_matrix=None, vocabulary=None, **count_vectoriser_args):
        self.ngram_range = ngram_range
        
        if term_doc_matrix is not None:
            if vocabulary is None: raise ValueError("term_doc_matrix supplied but no vocabulary!")
            self.term_doc_matrix = term_doc_matrix
            self.full_vocabulary = vocabulary
        else:
            if ngram_range is None or documents is None: 
                raise ValueError("Need to supply both ngram_range and documents if nothing to load!")
            
            default_cv_params = dict(strip_accents="unicode", lowercase=True, 
                                     max_df=1., min_df=0., max_features=None,
                                     stop_words=None)
        
            default_cv_params.update(count_vectoriser_args)
            if vocabulary is not None:
                default_cv_params["vocabulary"] = vocabulary
        
            vectoriser = CountVectorizer(ngram_range=ngram_range, **default_cv_params)
            self.term_doc_matrix = vectoriser.fit_transform(documents)
            self.full_vocabulary = vectoriser.vocabulary_
        
            print(f"{self}: Term Document Matrix constructed...")
        
        if precompute_freqs:
            self.term_freqs = self.term_doc_matrix.toarray().sum(0)
            print(f"{self}: Term frequencies precomputed...")
        else:
            self.term_freqs = None
        
        self.Ns = self.get_Ns()
        self.N = sum(self.Ns.values())
        
        
        self.analyzer = vectoriser.build_analyzer()
        
        
        print(f"{self}: Init done") 
        
    def iter_ngrams(self, doc, n, as_tuples=False):
        if not n in self.ngram_range:
            raise ValueError(str(self) + " not does not cover ngrams of length " + str(n))
        grams = self.analyzer(doc)
        f = filter(lambda s: s.count(" ") == (n-1), grams)
        if not as_tuples:
            return f
        return map(str.split, f)
            
    
    
    def get_Ns(self, ngram_range=None):
        l, h = ngram_range if (ngram_range is not None) else self.ngram_range
        rng = range(l, h+1)
        inds_per_n = (list(self.vocab(n, with_inds=True).values()) for n in rng)
        return {n: self.term_doc_matrix[:, inds].sum() for n, inds in zip(rng, inds_per_n)}
    
    
    
    def freq(self, *w):
        joined = " ".join(w)
        
        if not joined in self.vocab():
            raise ValueError(f"'{joined}' not in {self}'s vocabulary")

        if self.term_freqs is not None:
            return self.term_freqs[self.vocab()[joined]]
        return self.term_doc_matrix[:, self.vocab()[joined]].sum()    
    
    
    def prob(self, *w, log=False):        
        if not log:
            return self.freq(*w)/self.Ns[len(w)]
        
        return np.log2(self.freq(*w)) - np.log2(self.N)
    
    
    
    # let ws = (w_1, ..., w_k). computes p(w|w_1, ..., w_k) by #(<<w_1...w_k>w>)/#(<w_1...w_k>)
    def cond_prob(self, w, *ws, log=False):
        if not log:
            return self.freq(*ws, w)/self.freq(*ws)
        
        return np.log2(self.freq(*ws, w)) - np.log2(self.freq(*ws))
    
    
    
    
    
    
    
    
    
    
    def vocab(self, *ns, with_inds=False):
        if not ns :
            return self.full_vocabulary
        
        if not with_inds:
            return {w for w in self.full_vocabulary if len(w.split()) in ns} 
        
        return {w:i for w, i in self.full_vocabulary.items() if len(w.split()) in ns} 

    
            