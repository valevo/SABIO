# API Specification


## Introduction

(1) bias is a ubiqitous and complex phenomenon, it can pervade given (heterogeneous) data set at all levels, scales and dimensions  
(2) primarity because of (1), SABIO implements bias detection not as a monolithic algorithms but as collections of (preferrably) simple algorithms  

Because of (1), algorithms will operate on diverse types on input representations and similarly differ vastly in their output types; because of (2), i.e. the project's modular structure, algorithms will be added and replaced as an integral part of the development procedure. These reasons make it both important and useful to have clearly defined API, (1) for guiding the implementation of new algorithms, (2) to make SABIO transferrable to other sources of data and (3) to facilitate versatile and powerful user interfaces and visualisations.


## Types and Levels of Bias Navigation

#### types:
 
  - search: user wants to find examples of specific biases, find entities and concepts related to a specific bias (the user knows what they are looking for)
  - dicover: like search, except that the user does not yet know what the relevant inputs and parameter values are
  - explore: free-form, i.e. neither the search target nor the relevant heuristic or strategy is known by the user
  - quantify: obtain distributions, numeric measurements, etc that can e.g. be compared within the collection or across collections
  - compare/contrast: e.g. identify two subsets of the collection (e.g. based on meta-data properties) and compare them in terms of word association pairs


#### levels:
(non-exhaustive list)

  - text: lexical (e.g. word choices), semantic (word meanings), pragmatic (e.g. sentiments of sentences)
  - meta-data properties
  - individual samples (words, texts, objects, ...)
  - pairs of samples
  - (sub-) sets in the collection
  - connections in the collection
  - networks/graphs of objects/entities/concepts and their relations
  - distributions in the collection


#### data types 
(in the collection)

 - object: an entity in the [collection](https://collectie.wereldculturen.nl), a set of meta data properties: `{title, description, culture, origin, dimensions, inventory number, material, subcollection and keywords, ...}`
 - collection link: shared properties between objects (such as `material`, `keywords`), hierarchies according to `culture`, `origin`, `subcollection` 
 - textual entity: either a `title` or a `description`
 - concept: an entry in the [thesaurus](https://collectie.wereldculturen.nl/thesaurus), a set of concept properties: `{skos:prefLabel, skos:altLabel, skos:broader, skos:narrower, skos:scopeNote, skos:note, skos:notation, skos:inScheme, path, path - separate terms}
 - concept link: shared properties between concepts, hierarchies according to `broader` and `narrower`


## Modules/Engines


### Pointwise Mutual Information (PMI)

 - works on: pairs of words in textual entities, concepts

#### `compilation`

 procedure:  
 for each textual entity in the collection:
   - tokenise into a sequence of words -> build vocabulary
   - build word pairs
   - compute probabilities of: individual words & word pairs 

 parameters:
   - linguistic preprocessor functions (stemming, lemmatisation, normalisers)
   - tokeniser
   - list of words to exclude or equivalent function; maximum vocabulary size
   - maximum number of pairs

---
#### `inputs`/`parameters` for fine tuning

numeric:
 - PMI threshold 
 - frequency threshold
 - 

lists:
 - list of focus words
 - list of objects
 - list of meta-data properties
 
complex types:
 - subcollection, i.e. set of objects
 - 


--- 
#### `outputs`

(all corresponding to ceratin input/parameter values)

 - list of word pairs
 - list of textual entities
 - list of objects
 - distributions over word pairs, objects, ...
 - heatmap (e.g. indicating how many strong association pairs object an contains) over objects

---
#### specific `algorithms`

 - given a `threshold` -> `list of word pairs` which satisfy that threshold  
   -> goal: explore space of highly/lowly associated words
 - given a `list of words` -> `list of word pairs` that contain those words  
   -> goal: 
 - given a `list of textual entities`/`list of objects` -> `list of word pairs` in them which high PMI

 - given a `threshold` -> `list of textual entities`/`list of objects` which contain pairs which satisfy that threshold
 - given 



 
 
 
 
 
