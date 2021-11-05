import numpy as np
import scipy

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import nltk
stopwords = nltk.corpus.stopwords.words('dutch')

# TODO (?)
# 
# preprocessing:
#  - stemming
#  - proper segmentation for Dutch? (is subword encoding useful?)
# Smoothing? Add-one is simple enough. But then, we're only interested in the bigrams, so OOV unigrams will not arise
# 


class Ngram:
    def __repr__(self):
        return (f"{self.ngram_range}-grams")
    
#     # (1,1) is for only unigrams
#     # (2,2) is for only bigrams
#     # (1,2) is for unigrams and bigrams
#     # etc. 
#     def __init__(self, ngram_range, documents, precompute_freqs=False, **count_vectoriser_args):
#         self.ngram_range = ngram_range
        
#         default_cv_params = dict(strip_accents="unicode", lowercase=True, 
#                          max_df=1., min_df=0., max_features=None,
#                         stop_words=None)
        
#         default_cv_params.update(count_vectoriser_args)
        
#         self.vectoriser = CountVectorizer(ngram_range=ngram_range, **default_cv_params)
#         self.term_doc_matrix = self.vectoriser.fit_transform(documents)
# #         self.vocab = self.vectoriser.vocabulary_
        
#         print(f"{self}: Term Document Matrix constructed...")
        
#         if precompute_freqs:
#             self.term_freqs = self.term_doc_matrix.toarray().sum(0)
#             print(f"{self}: Term frequencies precomputed...")
#         else:
#             self.term_freqs = None
        
#         self.N = self.term_doc_matrix.sum()
#         print(f"{self}: Init done") 
        
        
    # (1,1) is for only unigrams
    # (2,2) is for only bigrams
    # (1,2) is for unigrams and bigrams
    # etc. 
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
        
        self.N = self.term_doc_matrix.sum()
        print(f"{self}: Init done") 
        
        
        
    def freq(self, *w):
        joined = " ".join(w)
        
        if not joined in self.vocab():
            raise ValueError(f"'{joined}' not in {self}'s vocabulary")

        if self.term_freqs is not None:
            return self.term_freqs[self.vocab()[joined]]
        return self.term_doc_matrix[:, self.vocab()[joined]].sum()
    
    
    def prob(self, *w, log=False):        
        if not log:
            return self.freq(*w)/self.N
        
        return np.log2(self.freq(*w)) - np.log2(self.N)
    
    
    # computes p(w2|w1) by #(<w1w2>)/#(w1)
    def cond_prob(self, w1, w2, log=False):
        if not log:
            return self.freq(w1, w2)/self.freq(w1)
        
        return np.log2(self.freq(w1, w2)) - np.log2(self.freq(w1))
    
    
    def pmi(self, w1, w2):
        return self.cond_prob(w1, w2, log=True) - self.prob(w2, log=True)

    
    def vocab(self, *ns, with_inds=False):
        if not ns :
            return self.full_vocabulary
        
        if not with_inds:
            return {w for w in self.full_vocabulary if len(w.split()) in ns} 
        
        return {w:i for w, i in self.full_vocabulary.items() if len(w.split()) in ns} 

    
    
    def save_matrix(self, path):
        scipy.sparse.save_npz(path, self.term_doc_matrix)
        
    @staticmethod
    def load_matrix(path):
        return scipy.sparse.load_npz(path)
    
    
    
    sep = "\t"
    
    
    def save_vocab(self, path, *vocab_ns, with_inds=False):
        sep = "<||>"
        sep = "\t"
        
        
        vocab = self.vocab(*vocab_ns, with_inds=with_inds)
        with open(path, "w") as handle:
            rest = lambda w: (sep + str(vocab[w])) if with_inds else ""
            for w in sorted(vocab):
                handle.write(str(w) + rest(w))
                handle.write("\n")        
            
#             if with_inds:
#                 for w, i in vocab:
#                     handle.write(str(w) + "\t" + str(i))
#                     handle.write("\n")
#             else:
#                 for w in vocab:
#                     handle.write(str(w))
#                     handle.write("\n")
    
    @staticmethod
    def load_vocab(path, with_inds=False):
        with open(path) as handle:
            lines = list(map(str.strip, handle))
            for l in lines:
                elems = l.split("\t")
                if with_inds:
                    yield elems[0], int(elems[1])
                else:
                    yield elems[0]

                    
    def save(self, name):
        self.save_matrix(name + ".npz")
        self.save_vocab(name + ".vocab", with_inds=True)
        
    @classmethod    
    def load(cls, name, precompute_freqs=False):
        td_mat = cls.load_matrix(name+".npz")
        voc = dict(cls.load_vocab(name+".vocab", with_inds=True))
        return cls(term_doc_matrix=td_mat, vocabulary=voc, precompute_freqs=precompute_freqs)
   
                    
#     @classmethod
#     def from_saved(cls, vocab_file, ngram_range, documents, precompute_freqs=False, **count_vectoriser_args):
#         vocab = cls.load_vocab(vocab_file, keep_inds=False)
        
#         return cls(ngram_range, documents, precompute_freqs=precompute_freqs, vocabulary=vocab)
   