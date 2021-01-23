# Manifesto

Detecting bias in texts of cultural signifcance, in particular with the aim to increase inclusivity in society, 
requires special care when designing detection algorithms. Therefore, below an incomplete and unordered list of things to be kept in mind.

It could be read as a kind of manifesto.


## Transparency

  1. Users must be able to understand *why* a certain decision was made, i.e. given which prior information or according to which metric bias was detected/
not detected.

  2. Users must be able to understand *where* a certain decision was made, i.e. which parts of the input lead the algorithm to detect/not detect bias.


## Scalability & Reproducibility

The strategies/algorithms designed in the scope of this project will likely only be able to address certain types and aspects of bias, e.g. be limited to bias against specific populations within society, and will have to ingore others. Since any bias detection strategy will be unable to detect all biases in all of their aspects, we require that: 

  1. The algorithms will have be readily adapted to biases that were not addressed in this project.
  
  2. The algorithms must clearly define their own borders in scope, i.e. if a certain type/aspect of bias was not explicitly addressed, then the algorithms should stay clear of it and not detect it.


## Accessibility

Biases affect all members of society and everyone can and should be provided with the possibility to benefit from our bias detection software, may that be 
through education about bias, for increasing visibility or for addressing injustices inflicted by bias. Therefore, the 

  1. The detection algorithms' processes and outputs must be presented in a way that maximises the number of users who can intuitively understand and 
  appropriately interpret them.
  
  2. The amount of technical knowledge, skill and effort for users to input their own data must be kept minimal so that a maximal number of users can 
  make use of the software.
  
  
