# Minimal Viable Product (MVP)

## SABIO: make social biases in heritage collections *more* accessible

Four terms to be clarified:
  - social biases: manifest in essentially all and any social and linguistic behaviours (require careful definition and especially strict delimitation)
  - heritage collections: our scope is focused on museums' collections, specifically those of heritage museums, and the aspects and types of bias that mainly arise there
  - accessible: on one hand equivalent to *visible*, i.e. making bias (as a whole or in its instances) *searchable*, *quantifiable*, etc <br>
     on the other hand, accessibility is about understanding, i.e. providing *context*, *explanation*, *alternatives* to bias
  - *more*: realising that bias is ubiquitous and in the limit impossible to detect, we only require that SABIO *increases* visibility of social bias

This is the central goal of SABIO, so we require this goal fulfilled by the MVP and all subsequent versions. The MVP and subsequent versions will differ mainly in the extent of their ability to provide access into bias. Since we choose a modular approach (both because for transparency and due to the nature of bias), developing subsequent versions out of the MVP will therefore consist mainly of adding new algorithms to increase visibility and context of bias. 

To be scaled up: The focus on heritage museums' collections actually make our task *easier*, since the data is highly curated and consists of linked data with persistent identifiers and thesauri. 


### Use Cases

We broadly distinguish *professionals* (collection managers, curators, social & historical researchers) and *end user* (general public, museum or website visitors).

*Active* use cases, i.e. those which assume that an example is already given or that a concept is known to contain bias:

 - professional is gathering examples of specific biases, e.g. usage examples within the collection of a term known to be contentious
 - professional seeks quantified characteristic, e.g. amount of bias associated with a concept, comparison of the biasedness in subsets of the collection
 - end user is unsure about a certain case of language use, e.g. whether used term should be considered contentious or not
 - end user requires context to a specific statement, e.g. 


Use cases that could be considered *passive*, in the sense that a professional/end user is trying to discover unconscious biases:

 - professional is trying to empirically define bias (in the heritage/historical contexts) 
 - professional searches for concepts or categories that fulfil a certain definition of bias or behave similarly to concepts that are known to contain biases
 - end user seeks to get an intuitive, empirical idea of bias means and how it might manifest
 - end user is interested which aspects of society are the most prominent in carrying bias


Moreover, we can categorise use cases into two aspects 
 
 - *quantitative*: indicating a degree to which a terms carries bias, the biasedness of a statement or a subset of the collection
 - *search*: finding terms which have larger-than-typical associations, contexts of terms or facts, subsets of the collection with similar properties



### Dimensions of Bias

For now, while we are in the development phase and because of the ubiquitous nature of bias, we cannot really talk about concrete programs (and it wouldn't make much sense). Since the discussion has to stay rather abstract, it is useful to identify some dimensions of such programs (the dimensions they 'live in'):

Note: At least for the MVP, we consider as 'data' the collection of the museum, including its specialised thesaurus. As a linked data set of descriptions, it consists of graph-like structures that describe objects' properties as text. That is, in brief, we are working on linked data on the one hand and linguistic data (i.e. text) on the other, and potentially on their interaction.

 1. 'level of bias': the level of the data that the focus is on; that is: type and representation of the input to the algorithms; words, word pairs, sentences, sets of sentences, word embeddings, graph nodes, graph relations, sets of graph relations, subsets of graphs, ...
 2. algorithms: the actual specific choice of an algorithm; the aspects of bias it is able to detect, how powerful it is in terms of accuracy and 
 3. the 'social' dimension: the categories of bias that are captured; gender, race, etc; whether the bias is offensive, positive, etc to those affected

Distinguishing these dimensions is important for defining an MVP (and thegeneral task), especially for transparency and explainability of the outputs of the MVP and subsequent versions. We require the MVP's output to clearly communicate these dimensions and how it works on each of them to the users which is naturally mainly a matter of the MVP's interface. It does, however, also imply that the back end and the algorithms used ensure to not entangle these dimensions (as much possible).

For the MVP, we try to stay as neutral as as possible to the third dimension. That is, rather than focussing on specific social categories, we seek to devise algorithms that are agnostic (to some extent) to these and detect biases regardless of social group, identity or quality of the bias. In doing so, we deviate from the body of previous work. Even though this is an ambitious objective, there is substantial leverage in the first two dimensions, for instance by omitting levels in data or by choosing less powerful algorithms. 


### Components

Strictly necessary components are:
  
  - back end, i.e. data ingestion and pre-processing
    - unified data structures
    - extraction and normalisation of text
    - linking of textual entities (NER), part-of-speech (POS) tagging, etc
    - ML-apt representations, such as embeddings
  - front end
    - search interface
    - visualisation of results and quantified characteristics
    - rich representations
    - illustration of algorithms

In between the back and the front end, at the core, lie the actual bias detection algorithms. Because of the modular approach, no/few will be actually strictly required and so below are only a few examples:

  - textual: 
    - implicit semantic associations: embedding-based, co-occurrence-based
    - paraphrase detection
    - sentiment analysis
  - graph-based:
    - expanding queries
    - graph algorithms: identifying cliques, shortest paths
    - associations
  - other: what other sources of data could be interesting/relevant/useful/important and algorithms working on them?


Because of the nature of the domain, viz. that bias is ubiquitous, the list of potential algorithms comprises essentially all of NLP and KG analysis (and probably beyond). This makes our project, once more, highly ambitious but as noted before, the modular approach we choose together with the different layers of the data we can focus on allow us to build a product step-by-step and do not require us to solve a monolithic task. This, in combination with the fact that the precise use cases of bias detection are still to be identfied, implies a development process built around experimentation. 


