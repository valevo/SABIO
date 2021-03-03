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









# Minimal Viable Product (MVP)

## SABIO: make social biases in heritage collections *more* accessible

Four terms to be clarified:
  - social biases: manfiest in essentially all and any social and linguistic behaviours, require careful definition and especially strict delimitation
  - heritage collections: our scope is focused on museums' collections, specifically those of heritage museums, and the aspects and types of bias that mainly arise there
  - accessible: on one hand equivalent to *visible*, i.e. making bias (as a whole or in its instances) *searchable*, *quantifiable*, etc <br>
     on the other hand, accessibility is about understanding, i.e. providing *context*, *explanation*, *alternatives* to bias
  - *more*: realising that bias is ubiquitous and in the limit impossible to detect, we only require that SABIO *increases* visibility of social bias

This is the central goal of SABIO, so we require this goal fulfilled by the MVP and all subsequent versions. The MVP and subsequent versions will differ mainly in extent 

Defining an MVP is therefore


Note: The focus on museums' data actually makes the task *easier* -> data is curated, linked, properly archived


### Uses Cases

We broadly distinguish *professionals* (collection managers, curators, social & historical researchers) and *end user* (general public, museum or website visitors).

 - professional is gathering examples of specific biases 
 - professional seeks quantified characteristic
 - end user is unsure about a certain case of language use
 - end user requires context to a specific statement



### Dimensions of Bias

For now, while we're in the development phase and because of the ubiquitous nature of bias, we can't really talk about concrete programs (and it wouldn't make much sense IMO). Since the discussion has to stay rather abstract, it is useful to identify some dimensions of such programs (dimensions 'they live in'):

Note: At least for the MVP, we consider as 'data' the collection of the museum, including its specialised thesaurus. As a linked data set of descriptions, it consists of graph-like structures that describe objects' properties as text. That is, in brief, we are working on linked data on the one hand and linguistic data (i.e. text) on the other, and potentially on their interaction.

 1. 'level of bias': the level of the data that the focus is on; that is: type and representation of the input to the algorithms; words, word pairs, sentences, sets of sentences, word embeddings, graph nodes, graph relations, sets of graph relations, subsets of graphs, ...
 2. algorithms: the actual specific choice of the algorithm; how powerful it is, 
 3. the 'social' dimension: the aspects of bias that captured; gender, race, offensive, positive, etc




### Components

 - back end: data ingestion: unified data structures, linking of entities (i.e. NER), extraction and normalisation of text
 - algorithms: 
   - textual:
   - graph-based:
   - other: are there any other sources of data that are interesting/relevant/useful/important?
 - front end: visualisation, search interface, illustration of statistics





