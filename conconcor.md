# CONtentious Words in CONtext CORpus (ConConCor)

## Notes & Questions

 - what about the following procedure: sample a random fragment `s` (=the context), then sample a (non-contiguous) span `p` from `s`; the task for the participant is then to rate contentiousness  
   => as opposed to the participant identifying spans by themselves  
   -> could remedy the problem that it may be too unclear to the paricipants what 'contentiousness' implies for the task 
   -> potential problem: most spans will not be contentious, i.e. waste of time & may influence the 'contentiousness baseline'

 - require diversity in the group of annotators  
   -> contentiousness as the sum of what the society considers as such  
   -> what information do we want to ask from participants?



## Annotation Scheme

#### References

 - [GRaSP: A Multilayered Annotation Scheme for Perspectives](http://www.lrec-conf.org/proceedings/lrec2016/pdf/469_Paper.pdf)  
   -> paper from the VU (Aroyo and others)  
   -> *Section 3.1: 'Our perspective annotations are aimed at capturing the attitude of a source towards some target.'*




#### Most Basic Version

for each phrase `p` in each sentence `s`:
  - is `p` contentious?
  - if so, required: score of contentiousness
  - if so, optional: preferred alternative
  - if so, optional: explanation

where `p` is any (possibly non-contiguous) span of characters in `s`



#### Potential Difficulties

 - phrases with complex spans (includes uncertainty about predcise span)
 - perspective/voice (e.g. indirect speech)
 - conentiousness is implicit in the sentence (e.g. "all X are Y")
 -  




## Choice of Annotation Platform

The choice of annotation tool will certainly influence the annotation scheme (at least in terms of input/output formats).


 - BRAT? needs to be self-hosted, someone at UvA set that up which actually a fork from someone at KNAW



## Pilot Experiments: Evaluating Algorithms & Bootstrapping Models

The point of the pilot experiments is to exemplify uses and the importance of data sets such as ConConCor. They also serve to investigate the usefulness of ConConCor, i.e. whether or not they can be meaningfully applied to bias detection and Culturally Aware AI. They're pilot experiments in the sense that they will check for basic properties and types of algorithms. 

A major use, based on the representativeness of ConConCor, is the evaluation of the mehtods ad algorithms developed in the context of SABIO and Culturally Aware AI: Whether these methods can reproduce the terms annotated 

CAUTION: ConConCor is about contentiousness which is partly a subset of bias and partly a different concept, namely when bias stops being bias and turns into violence (consider offensive terms). In other words, the concept of contentiousness can be seen as capturing certain aspects of bias but also extending beyond it.


#### Ideas

 1. Bootstrap CTR (contentious term recognition) model:  
     - binary decision function 
     - may be a transformer head (e.g. a binary output head on BERTje)  
       -> consider one annotated span (i.e. a binary vector of size sentence length) as an example, enrich with negative sampling
     - use CTR model as point of comparison for a evaluation of deterministic/parameter-free/non/black-box algorithm  
       (to answer the question _how good can any model be on this task?_)
 
 2. Evaluate Algorithms
     - point is: algorithms that deal with bias should mainly be unsupervised learners or perform no 'learning' in the ML sense at all (mainly for transparency and lack of training data) 

 3. some experiment should make use of the contentiousness scores... perhaps correlate contentiousness with sentiment (the output of a sentiment anaylser)?
 4. some experiment should make use of the preferred alternatives... perhaps: exchange contentious terms by their preferred alternatives, then measure biasedness of the oontext (or sentiment)?


#### Potential Difficulties

 - span selected by annotator (star chars-end chars) may not match tokeniser's decisions
 - non-contiguous spans 



