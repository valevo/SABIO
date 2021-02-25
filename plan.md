# SABIO Project Plan

# Step 0

## Practical Work a.k.a. Programming
 - process the meta-data network, automate common patterns
 - gather characterstics of the dataset -> will point towards types of methods, might reveal problems that need to be be addressed
 - do some basic experiments such as term tracking, dependency parsing, etc -> will restrict and/or guide the choice of algorithms
   - automate term tracking -> probably useful in any case
   - gather tasks from basic experiments in suite of tools (& set up properly)
 - pre-process the linguistic data, the objects' descriptions, including vectorisation and (basic) feature extraction


## Theoretical Work a.k.a. Conceptual Analysis and Formalisation

 - map experts' perspectives on social bias (domain experts are philosophers, social scientists, activists, *really anyone but me*):
   - get a workable definition which can be translated into linguistic/statistical properties
   - define boundaries of bias in opposition to other concepts
   
 - manifesto: carefully explicate our own goals and requirements to (1) be judged against and (2) make process transparent and reproducible

 - review previous work: 
   - already identified domains, problems and formalisations 
   - inspiration from methods already in use
   - off-the-shelf algorithms and libraries
   - limitations 
   
 - formalise the world of biases (types, aspects, levels) to be detected in the first iteration 
   
##### => goal for February: be ready to implement a battery of detection algorithms for experimentation and feedback from the stakeholders 
 
 

# Step 1

TBD









# Minimal Viable Products

## SABIO: make social biases in heritage collections *more* accessible

Four terms to be clarified:
  - social biases: manfiest in essentially all of social and linguistic behaviours, require careful definition and especially strict delimitation
  - heritage collections: our scope is focused on museums' collections, specifically those of heritage museums, and the aspects and types of bias that mainly arise there
  - accessible: on one hand equivalent to *visible*, i.e. making bias (as a whole or in its instances) *searchable*, *quantifiable*, etc <br>
     on the other hand, accessibility is about understanding, i.e. providing *context*, *explanation*, *alternatives* to bias
  - *more*: realising that bias is ubiquitous and in the limit impossible to detect, we only require that SABIO *increases* visibility of social bias




## Uses Cases

Broadly distinguish professionals (collection managers, curators, social & historical researchers) and end user (general public, museum or website visitors).

 - professional is gathering examples of specific biases 
 - professional seeks quantified characteristic
 - end user is 



### Components

 - back end: data ingestion: unified data structures, linking of entities (i.e. NER), extraction and normalisation of text
 - algorithms: 
 - front end: visualisation, search interface, illustration of statistics





