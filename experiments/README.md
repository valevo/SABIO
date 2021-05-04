# Experiments



## [ex1](ex1/): PMI

Experiments into using [PMI](https://en.wikipedia.org/wiki/Pointwise_mutual_information), which measures collocation of word pairs, to detect lexical semantic bias. Bias is thus operationalised as the amount and directionality of co-occurrence-based association between pairs of words.

PMI ranges from negative to positive infinity, with PMI = 0 if and only if two words are independent from each other. Negative PMI implies that two words 'repeal' each other, i.e. their chance of occurring together is lower than would have been expected.  

PMI can be useful to find the associations of a given word, or to explore which pairs of high association exist in the corpus. In both cases, we first construct the full table of all associations between all pairs and then eliminate entries based on relevance, such as word classes, semantic features, etc. 


### Algorithm

 1. compute P(w) & P(w|w') for all observed words w and observed word pairs w and w'
 2. compute PMI(w, w') = log P(w|w') - log P(w) for all pairs w and w'
 3. sort all pairs according to PMI



#### TODOs

 - do proper linguistic analysis: stemming or even lemmatisation, more sophistcated semgentation (-> split compounds)
 - more sophisticated pairing, e.g. based on dependency parse

 - find concordances: given an n-gram, get set of:
   - documents in which n-gram occurs (sorted by some criterion)
   - high-ranking n-grams which occur in the same document

 - could be interesting: PMI is symmetric in its arguments (since mutual information is)  
   -> are there asymmetric versions? Would be useful since lexical semantic bias probably is; possible candidate: [Delta P](https://www.degruyter.com/document/doi/10.1515/cllt-2017-0036/html)
   


## [ex2](ex2/): Semantic Spaces 

Vector space as the place where words/phrases "live":

 - measures on vector space can be correlated/paralleled with other measures, e.g. cosine similarity and PMI
 - interface between visual and textual worlds
 - words/phrases are co-indentified by a vector and a record: 



In combination with PMI: cluster unigrams into `k` clusters, then compute top `m` pairs (`w1, w2`) with highest PMI s.t. that `w1` and `w2` are *not* in the same cluster  
-> have count vectors anyway  
-> use tf-idf or maybe even topic modelling for the vector projections (and even the clustering)
=> this is our operationalisation of (lexical semantic) bias: PMI measure strength of bias, the clusters define semantic classes and bias is equivalent to associations between (exemplars of) different classes
=> can make this more general by not using clusters but distance instead (i.e. top pairs (`w1`, `w2`) s.t. `PMI(w1, w2)` is maximised and `d(w1, w2)` and is above some threshold



## ex3: Linked Data & Querying

Initial experiment into linked data search and querying: Using the terms from the *Words Matter* publication, track them across the collection. That is for each term, find terms that tend to correlate or that are otherwise related and in this way build up a small network for the term.

This experiment is also meant as an exercise to see what potentials *Words Matter* has for designing algorithms. And to judge the possibilty of adding new terms to *Words Matter* based on such algorithms.


## [ex4](ex4/): Typicality

Using typicality.
