# CONtentious Words in CONtext CORpus (ConConCor)

## Data Selection

 - [interesting example about the use of the word "Bosneger" provided by Andrei](https://www.delpher.nl/nl/kranten/view?query=bosneger&coll=ddd&identifier=ddd:110587315:mpeg21:a0154&resultsidentifier=ddd:110587315:mpeg21:a0154&rowid=8)
 

### TODO

 - implement typicality as a sampling strategy to be used in combination with Ryan's stratified sampling schemes  
   -> either use to completely disregard certain parts of the data, or as sampling weight  
   -> can also help analyse data set for their "normality"
 
 - the data set contains a substantial amount of serious OCR errors  
   -> use dictionary method to filter sentences which contain words that are not in the dictionary  
   -> use subword encoders to judge the probabilty of individual character sequences
   



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

where `p` is any (possibly non-contiguous) span of characters in `s`, i.e. for any (ordered) set of indices `{i_1, ..., i_k} \subset |s|`, `p = (w_i_1, ..., w_i_k)` is a candidate phrase. 



#### Potential Difficulties

 - phrases with complex spans (including uncertainty about predcise span)
 - perspective/voice (e.g. indirect speech)
 - conentiousness is implicit in the sentence (e.g. "all X are Y")




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


 - the original BERTje paper did sentiment analysis, cites a Dutch corpus of sentiments and reports scores -> is the trained analyser available somewhere?  
   -> ULMFiT does even better than BERTje, maybe that has pretrained sentiment analysis available for Dutch?

#### Potential Difficulties

 - span selected by annotator (star chars-end chars) may not match tokeniser's decisions
 - non-contiguous spans 



