# CONtentious Words in CONtext CORpus (ConConCor)



## Annotation Scheme

#### References

 - (GRaSP: A Multilayered Annotation Scheme for Perspectives)[http://www.lrec-conf.org/proceedings/lrec2016/pdf/469_Paper.pdf]  
   -> paper from the VU (Aroyo and others)  
   -> *Section 3.1: 'Our perspective annotations are aimed at capturing the attitude of a source towards some target.'*




#### Most Basic Version

for each phrase `p` in each sentence `s`:
  - is `p` contentious?
  - if so, required: score of contentiousness
  - if so, optional: preferred alternative
  - if so, optional: explanation

where `p` is any non-contiguous



#### Potential Difficulties

 - phrases with complex spans (includes uncertainty about predcise span)
 - perspective/voice (e.g. indirect speech)
 - conentiousness is implicit in the sentence (e.g. "all X are Y")
 -  




## Choice of Annotation Platform

 - BRAT? needs to be self-hosted, someone at UvA set that up which actually a fork from someone at KNAW



## Pilot Experiments: Evaluating Algorithms & Bootstrapping Models


#### Ideas

 1. Bootstrap CTR (contentious term recognition) model:  
   - binary decision function 
   - may be a transformer head (e.g. a binary output head on BERTje)  
     -> consider one annotated span (i.e. a binary vector of size sentence length) as an example, enrich with negative sampling
   - use CTR model as point of comparison for a evaluation of deterministic/parameter-free/non/black-box algorithm  
     (to answer the question _how good can any model be on this task?_)
 
 2. Evaluate Algorithms
   - point is: algorithms that deal with bias should mainly be unsupervised learners or perform no 'learning' in the ML sense at all (mainly for transparency and lack of training data) 


#### Potential Difficulties

 - span selected by annotator (star chars-end chars) may not match tokeniser's decisions
 - non-contiguous spans 




