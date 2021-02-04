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
  
  Making use of the fact that Dutch marks gender in its vocabulary (via fusional morphology): 
  
  
