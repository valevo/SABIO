# Manifesto

Detecting bias in texts of cultural signifcance, in particular with the aim to increase inclusivity in society, 
requires special care when designing detection algorithms. Therefore, below an incomplete and unordered list of things to be kept in mind.

It could be read as a kind of manifesto.


## Transparency

decision are not clear cut, sometimes not even well-defined, there is no universally agreed truth -> decisions are not easily judged to be correct or false, especially not if decision process is opaque

bias detection is not purely about usage (as opposed to self-driving cars) but also about forming opinion -> like anywhere else, an opinion requires argument and justifaction



  1. Users must be able to understand *why* a certain decision was made, i.e. given which prior information or according to which metric bias was detected/
not detected.

  2. Users must be able to understand *where* a certain decision was made, i.e. which parts of the input lead the algorithm to detect/not detect bias.


## Scalability & Reproducibility

The strategies/algorithms designed in the scope of this project will likely only be able to address certain types and aspects of bias, e.g. be limited to bias against specific populations within society, and will have to ingore others. Since any bias detection strategy will be unable to detect all biases in all of their aspects, we require that: 

  1. The algorithms will have be readily adapted to biases that were not addressed in this project.
  
  2. The algorithms must clearly define their own borders in scope, i.e. if a certain type/aspect of bias was not explicitly addressed, then the algorithms should stay clear of it and not detect it.


## Accessibility

Biases affect all members of society and everyone can and should be provided with the possibility to benefit from our bias detection software, may that be 
through education about bias, for increasing visibility or for addressing injustices inflicted by bias. Therefore:

  1. The detection algorithms' processes and outputs must be presented in a way that maximises the number of users who can intuitively understand and 
  appropriately interpret them.
  
  2. The amount of technical knowledge, skill and effort for users to input their own data must be kept minimal so that a maximal number of users can 
  make use of the software.
  
  
## Democratisation

precisely because bias affects everyone: & because of what is mentioned in Section **Transparency**, we need society to define what a bias detection tool does and should do 


  1. design decision should, where possible, be informed by larger concensus, may thatfor instance be directly democratic process or (academic) concensus
  
  2. in the interest of the protection of minorities, public inputs should not be directly integrated into our software but via a curative process (to avoid e.g. the nature of publicly voiced opinion on internet forums); eventually, harm is to be avoided and this requirement extends to user inputs
  
  

 
 
 
# Notes for the manifesto

 - democratise (see section **Democratisation**) the process by which this manifesto is built -> create protocol by which users can provide input/feedback
 
 - add numbering/prioritisation (doesn't need to be an absolute/fixed/deterministic ordering) to sections
 
 - related to above point: use Optimality Theory on these requirements -> create a formalised process for design decisions (program\_1 violates {req\_1, req\_3}, program\_2 violates {req\_2}) 
 
 - find sources from philosophy that have something to say about this (FAIR principles?, ethics of AI?) <br>
 -> the manifesto then becomes the interface between philosophy and our "AI"
 -> talk to Mrinalini and Julia
 


## Potential Resources

 - [[Shah et al. 2019]](#1) surveys, maps and formalises the potential sources and guises of bias in NLP models
 
 - the FAIR principles
 

<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 
<br>
bla bla bla bla bla bla bla bla bla bla bla bla bla bla bla 

 
 
 


## Referencs
  <a id="Shah et al. 2019">1. </a> 
  Shah, D., Schwartz, H. A., & Hovy, D. (2019). Predictive biases in natural language processing models: A conceptual framework and overview. arXiv preprint arXiv:1912.11078.
  



  
