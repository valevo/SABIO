# The Theory of SociAl BIas Observation 

This is a work-in-progress guide to the theoretical aspects of SABIO. Here, we describe conceptual and theoretical work and ideas. 

## [Manifesto](manifesto.md)

As SABIO, and Cultural AI in general, are located deeply in the domain of responsible AI, it is an important value that our process is transparent and fair. To even add an activist stance on top, we are creating a manifesto for how cultural AI should be done and what it should and should not be.


## [Defining Bias](defining_bias.md)

In order to detect it, we need to first find a definition of bias. This will be a *working* definition, i.e. while it may not withstand strict philosophical criticism, its purpose is to serve as an interface between the rigid world of algorithms and our layered, complex and continuous (social) world.


## [Heuristics](heuristics.md)

Owing to both its pervasive and evasive nature, an immense plethora of algorithms are potentially viable for or useful towards bias detection; arguably almost all of machine learning in fact. Furthermore, with the intention of transparency and explainability, we opt for a very modular approach to bias detection. And so for these reasons, many heuristics are interesting for SABIO.

 

## Random Ideas  
 
Put here for now, to be sorted later.  
   
## Social Bias versus Statistical Bias

It is not really a coincidence that both statisticians and social scientists speak of bias. 
In statistics, bias is a type of systematic difference of an estimator from the true value; formally, the expected value of a statistic *T* can be expressed as *E[T] = \theta + bias(T, \theta)*  and *T* is unbiased wrt. the theoretical value *\theta* iff *bias(T, \theta) = 0*.
In social science or philosophy, bias (**WHAT IS SOCIAL BIAS EXACTLY?**).

-> Perhaps we leverage this coincidence of terms and underlying concepts? Social bias is (probably) very difficult to operationalise directly, but could we perhaps use statistical bias, which is straighforwardly measurable, as a proxy for social bias? That is, we would construct a random variable whose theoretical value is known and a statistic such that the statistical bias of the statistic is equivalent to a social bias. <br>

*Example*: Our random variable is the difference is co-occurrence probability of a word *W* with the words *man* and *woman*, *v = |P(W|man) - P(W|woman)|*, of which we would expect that its value is 0 (*P(v=0)=1*) if language is unbiased. Given a corpus *C*, we can construct the statistic *T(C) = |#(W|man, C) - #(W|woman, C)|* of which the expected value over all corpora is *E[T] = \sum_C P(C)*T(C) = v + bias(v)*



 
## Test Data
  
  
  Is there a way to obtain test data, to be able to make the successfulness/appropriateness of whatever approaches we choose/develop measurable?
  This could be data created and/or annotated by others, or our own data measured along some proxy (or both).
  
  Assuming that there is no data annotated for bias itself, a possible sketch could be:  
    
  
  
## Language without Bias?

Quantifying bias has a similar problem as the quantification of laws (e.g. Zipf's) in language: Because they are intrinsic properties of language, it is impossible to imagine languages where bias or laws (such as Zipf's) don't exist. The very practical problem arises then that a measured value of quantification becomes somewhat meaningless because it has no "null" point that it can be studied in comparison of. (I.e. what does a biasedness value of 10 mean if I don't know what the sample would need to look like to obtain a value of 0.)

=> This [paper](https://github.com/valevo/SABIO/blob/main/papers.md#understanding-the-origins-of-bias-in-word-embeddings) on removing parts of a corpus whose removal would most reduce bias could offer help here. Namely that by removing and re-measuring bias, we can obtain estimates of the derivative of the measuring function at the point defined by the particular corpus. Thereby, we get at least an idea of how our measurement from the original corpus relates to (hypothetical) measurements from other corpora, we contextualise our measurement. (This is also related to statistical techniques such as bootstrapping.)

=> The concept of Typicality (of Typical Set) from Information Theory can also be useful to address the same issue. If we could figure out the probability of a (sub-)corpus as a function of the bias it contains, we directly use Typicality to quantify bias and to samples with less (/more) bias.


## Bias as the Adversary

Could bias detection be phrased as an adversarial learning problem? What would the adversary's loss be?
Perhaps considering a scenario where language is always bias-free but then an adversary adds bias before it is uttered? -> trick the adversary 
Or perhaps an adversary could be used just to improve the performance of detection algorithms? I.e. as an additional loss 


