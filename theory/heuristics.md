# A Random Collection of heuristics


## Ensemble Strategies

It seems a good idea to invoke an ensemble of strategies/heuristics rather than a monolithic one, because 

  1) with the scope of our project quite limited implementing a battery of small algorithms mitigates risk
  2) simple individual strategies have individually higher chances of being correct and uncontroversial in their decision making
  3) modularity, which is inherent in an ensemble approach, leads to higher chance of reuse and further improvement by others
  4) transparency is typically most readily achieved in simple algorithms
  
The individual heurstics can complement each other in the types and levels of bias they work on and those heuristics whose decisions may contradict each other
can, much in the spirit of ensemble learning, be weighted and aggregated. In a similar vein, and perhaps contigent on the availability of test data or human
feedback, the individual strategies can be evaluated independently and in comparison.

Thus, the heuristics/strategies/algorithms sketched below are chiefly aimed at individual parts of a full bias detection process.


## Leveraging ML Models' Biases
  
  *Note: a basic and rather obvious idea but still worth describing and formalising properly*
  
  Quite some of the work on bias in the computational domain is about the bias exhibited by ML models, how such models inherit the biases present in society. We could
  leverage this body of work in order to quantify bias in our datasets. Namely by training models on our data and then investigating the bias these models have acquired
  with the methods put forward by the papers in this line of work. 
  
  Specifically, this can be applied to continuous, vector representations (of words and/or sentences): Train a language model from scratch on our corpus, then inspect
  and compare the learned representations by the proposed methods. Further, the corpus-specific representations can be compared to representations obtained 
  
  Important assumptions:
   
   - the bias exhibited by the trained model is (completely) the bias in the data, and not introduced by the model
    
    
  
  
## Predictive Model for Gender Bias
  
  Making use of the fact that Dutch marks gender in its vocabulary (via fusional morphology). See this [abstract by Laura](https://ir.cwi.nl/pub/29761) in which they propose basically exactly this idea. Unfortunately never actually got carry out the experiments described there.





## Bayesianism

Bias could potentially be neatly operationalised as (too much/to little) probability mass; by explicitly distinguishing prior and likelihood (via Bayes), we could access to overall bias (reflected in the prior) and contextual bias (reflected in the likelihood). <br>
To give an simple (and stupid) example: We compare *P(man|doctor)* and *P(woman|doctor)* which are, respectively, prop. to *P(man)*P(doctor|man)* and *P(woman)*P(doctor|woman)*. *P(man)* vs *P(woman)* is global bias, i.e. *P(man) > P(woman)* corresponds to overrepresentation of men (and underrepresentation of women). Similary, *P(doctor|man)* and *P(doctor|woman)* is contextual bias, i.e. if *P(doctor|man) > P(doctor|woman)* then 

## Randomness

Bias likely manifests itself as a lack of randomness with respect to some distributions. Although this is rather vague, randomness testing could be a useful family of techniques. As advantages, these are typically easy to apply and offer large degrees of objectivity and some degrees of transparency. Moreover, they are related to the Bayesian approach and thus can be easily done dually.  




## Bias in Network via Queries

 - randomly sample (construct) queries into the network, compute statistics on results -> expected outcome: some items (or properties of items) will be over-represented and some under-represented, so what do these says about (types of) biases?
 - this is reminiscient of an MCMC method -> thus the question: what distribution are we sampling by this procedure?
 - Marieke mentioned similar research, namely [this paper by Jacco](https://ieeexplore.ieee.org/abstract/document/7559558)
 - nice thing: depending on the sampling procedure, this method is fairly objective and unbiased in itself
  
