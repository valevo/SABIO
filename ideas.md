  # Random Ideas 
  
  
  ## Leveraging ML Models' Biases
  
  *Note: a basic and rather obvious idea but still worth describing and formalising properly*
  
  Quite some of the work on bias in the computational domain is about the bias exhibited by ML models, how such models inherit the biases present in society. We could
  leverage this body of work in order to quantify bias in our datasets. Namely by training models on our data and then investigating the bias these models have acquired
  with the methods put forward by the papers in this line of work. 
  
  Specifically, this can be applied to continuous, vector representations (of words and/or sentences): Train a language model from scratch on our corpus, then inspect
  and compare the learned representations by the proposed methods. Further, the corpus-specific representations can be compared to representations obtained 
  
  Important assumptions:
    - the bias exhibited by the trained model is (completely) the bias 
    
  
  
