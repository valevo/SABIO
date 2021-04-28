# API Specification


## Introduction

(1) bias is a ubiqitous and conplex phenomenon, it can pervade given (heterogeneous) data set at all levels, scales and dimensions  
(2) primarity because of (1), SABIO implements bias detection not as a monolithic algorithms but as collections of (preferrably, for introspection) simple algorithms  

Because of (1), algorithms will operate on diverse types on input representations and similarly differ vastly in their output types; because of (2), i.e. the project's modular structure, algorithms will be added and replaced as an integral part of the development procedure. These reasons make it both important and useful to have clearly defined API, (1) for guiding the implementation of new algorithms, (2) to make SABIO transferrable to other sources of data and (3) to facilitate versatile and powerful user interfaces and visualisations.




## Definitions

#### Data Types in the Collection

 - object: an entity in the [collection](https://collectie.wereldculturen.nl), a set of meta data properties: `{title, description, culture, origin, dimensions, inventory number, material, subcollection and keywords, ...}`
 - collection link: shared properties between objects (such as `material`, `keywords`), hierarchies according to `culture`, `origin`, `subcollection` 
 - textual entity: either a `title` or a `description`
 - concept: an entry in the [thesaurus](https://collectie.wereldculturen.nl/thesaurus), a set of concept properties: `{skos:prefLabel, skos:altLabel, skos:broader, skos:narrower, skos:scopeNote, skos:note, skos:notation, skos:inScheme, path, path - separate terms}
 - concept link: shared properties between concepts, hierarchies according to `broader` and `narrower`





## Modules


### Pointwise Mutual Information (PMI)

 - works on: pairs of words in textual entities, concepts

#### `preparation`

 for all textual entities:
   - tokenise into a sequence of words -> build vocabulary
   - build word pairs
   - compute probabilities of: individual words & word pairs 

#### `inputs`/`parameters`


 - PMI threshold
 - frequency threshold

 - list of focus words


 - list of objects
 - subcollection, i.e. set of objects
 - list of meta-data properties

 
#### `outputs`

all corresponding to ceratin input/parameter values

 - list of word pairs
 - list of textual entities
 - list of objects
 - distributions over word pairs, objects, ...
 
 
 
 
 
