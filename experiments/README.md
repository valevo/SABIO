# Experiments


## [ex1](ex1.ipynb)

Initial experiment into using [PMI](https://en.wikipedia.org/wiki/Pointwise_mutual_information), which measures collocation of word pairs, to detect lexical semantic bias.
First, generate the full `n x n` matrix of PMI values, then eliminate according to PMI value itself, word classes, etc.

Could be interesting: PMI is symmetric in its arguments (since mutual information is) -> are there asymmetric versions? Would be useful since lexical semantic bias probably is. Possible candidate: [Delta P](https://www.degruyter.com/document/doi/10.1515/cllt-2017-0036/html).
