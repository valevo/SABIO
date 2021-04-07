# Experiments


## [ex1](ex1/)

Initial experiment into using [PMI](https://en.wikipedia.org/wiki/Pointwise_mutual_information), which measures collocation of word pairs, to detect lexical semantic bias.
First, generate the full `n x n` matrix of PMI values, then eliminate according to PMI value itself, word classes, etc.

Could be interesting: PMI is symmetric in its arguments (since mutual information is) -> are there asymmetric versions? Would be useful since lexical semantic bias probably is. Possible candidate: [Delta P](https://www.degruyter.com/document/doi/10.1515/cllt-2017-0036/html).

### Idea
In combination with PMI: cluster unigrams into `k` clusters, then compute top `m` pairs (`w1, w2`) with highest PMI s.t. that `w1` and `w2` are *not* in the same cluster  
-> have count vectors anyway  
-> use tf-idf or maybe even topic modelling for the vector projections (and even the clustering)
=> this is our operationalisation of (lexical semantic) bias: PMI measure strength of bias, the clusters define semantic classes and bias is equivalent to associations between (exemplars of) different classes
=> can make this more general by not using clusters but distance instead (i.e. top pairs (`w1`, `w2`) s.t. `PMI(w1, w2)` is maximised and `d(w1, w2)` and is above some threshold


### TODO

 - given an n-gram, get iterator over documents in which n-gram occurs (sorted by some criterion)
 - given an n-gram, get iterator over high-ranking n-grams which occur in the same document



## ex2

Initial experiment into linked data search and querying: Using the terms from the *Words Matter* publication, track them across the collection. That is for each term, find terms that tend to correlate or that are otherwise related and in this way build up a small network for the term.

This experiment is also meant as an exercise to see what potentials *Words Matter* has for designing algorithms. And to judge the possibilty of adding new terms to *Words Matter* based on such algorithms.
