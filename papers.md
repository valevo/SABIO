
Andrei's resources on [GDrive](https://drive.google.com/drive/u/0/folders/1ncPfsOL_WmAUnGbEbqMMFAw1sF32gTLw)

Ryan's resources on [GitHub](https://github.com/ryanbrate/phd_reading_list)


## General Notes

- relatively little literature seems concerned with the task of detecting bias in corpora for the purpose of (synchronic) linguistic or sociological investigation
  or even for addressing **human** bias by making it visible; instead there seem to be two lines:
  
  - substantial efforts are starting to arise in quantifying, qualifying and mitigating bias for ML purposes, i.e. to address the bias that machines learn from humans and to try to develop machines that have as little bias as possible (and necessary, since learning without bias can be argued to be impossible) <br>
  here, there is some work on bias in corpora itself but only in the sense of corpora as training data
  
  - one more linguistically inclined line seems to be diachronic investigation of bias, i.e. to track how bias evolves through time; this is of course a subdiscipline of computational studies of the evolution of meaning
  
  
  
# Fairness

## A Statistical Test for Probabilistic Fairness

Theoretical paper which derives statistical tests for classifier functions. Could be useful for inspiration and for theoretical motivation; published at FAccT 2021. 

[Link to PDF](https://arxiv.org/pdf/2012.04800.pdf) | [BibTeX Entry](https://scholar.googleusercontent.com/scholar.bib?q=info:tkrrAOA23qwJ:scholar.google.com/&output=citation&scisdr=CgXMhBClEPb21fB7y4A:AAGBfm0AAAAAYAl-04D1aEEMTGr9aOP2qbQNlfhBi2iG&scisig=AAGBfm0AAAAAYAl-06ChVPXETeDZLX5BNYwB5BBv4qhd&scisf=4&ct=citation&cd=-1&hl=en)


## 50 Years of Test (Un)fairness: Lessons for Machine Learning

Review (plus opinions) of the history of formalising *fairness*, especially in contexts of statistics and computational analysis. Includes a formal comparsion framework.

[Link to PDF](http://www.m-mitchell.com/papers/History_of_Fairness-arxiv.pdf) | [BibTeX Entry](https://scholar.googleusercontent.com/scholar.bib?q=info:Oa1R0kHeAREJ:scholar.google.com/&output=citation&scisdr=CgXMhBClEPb21ekT888:AAGBfm0AAAAAYBAW68-vQKNCvDHwHqVKNk45S_opyVJS&scisig=AAGBfm0AAAAAYBAW64oA4STFAnmZX8C37dJWj2zlp7--&scisf=4&ct=citation&cd=-1&hl=en)


## On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?

Critical paper on the rise of massive LMs that sheds light on problems that arise from the practice of estimating billions and trillions of parameters from hundreds of gigabytes of data. Among these problems the social biases that are perpetuated by such models. Received additional attention as Google lead employees, two of the authors, were put under pressure for writing this paper.

[Link to PDF](http://faculty.washington.edu/ebender/papers/Stochastic_Parrots.pdf) | [BibTeX Entry](https://scholar.googleusercontent.com/scholar.bib?q=info:-frkS3CfwgUJ:scholar.google.com/&output=citation&scisdr=CgXMhBClEPb21ekfuwg:AAGBfm0AAAAAYBAaowiWuqHRHWqYNL02PhQLYkw96dcI&scisig=AAGBfm0AAAAAYBAao6YQ_jKYoMyy-rDBoKFm0FQ8kNLm&scisf=4&ct=citation&cd=-1&hl=en)




## Mitigating Unwanted Biases with Adversarial Learning

Should be self-explanatory; potentially interesting for: 
  - addressing bias in the sense of mitigating it and formalisation thereof
  - adversarial framework
  - the resources mentioned in this paper


[Link to PDF](http://www.m-mitchell.com/papers/Adversarial_Bias_Mitigation.pdf) | [BibTeX Entry](https://scholar.googleusercontent.com/scholar.bib?q=info:v4k0PGBZBJgJ:scholar.google.com/&output=citation&scisdr=CgXMhBClEPb21ek1gew:AAGBfm0AAAAAYBAwmew8tGaw4KUMcESXaKWxQcf0-w7N&scisig=AAGBfm0AAAAAYBAwmSGoxx5v9NxxLiuMThvaImaiyd22&scisf=4&ct=citation&cd=-1&hl=en)



## Language (Technology) is Power: A Critical Survey of “Bias” in NLP

Extensive survey of papers about adressing bias in NLP (models) that finds vagueness and inconsistency across this landscape of papers.


[Link to PDF](https://arxiv.org/pdf/2005.14050.pdf) | [BibTeX](https://scholar.googleusercontent.com/scholar.bib?q=info:crDf6GtBo8oJ:scholar.google.com/&output=citation&scisdr=CgXMhBClEPb21elPPTk:AAGBfm0AAAAAYBBKJTlOhrbRn-kBQ-XL3jDSk4kL4jvq&scisig=AAGBfm0AAAAAYBBKJfanTEUyzCXUETRoRYMxqn4ae9vH&scisf=4&ct=citation&cd=-1&hl=en)



## Race and Gender

Critical review by Timnit Gebru on the role of science, specifically AI, in social issue, specifically race and gender. Chapter of the [Oxford Handbook of Ethics of AI](https://www.oxfordhandbooks.com/view/10.1093/oxfordhb/9780190067397.001.0001/oxfordhb-9780190067397).

[Link to PDF](https://arxiv.org/ftp/arxiv/papers/1908/1908.06165.pdf) | [BibTeX Entry](https://scholar.googleusercontent.com/scholar.bib?q=info:8XiuL9kXndgJ:scholar.google.com/&output=citation&scisdr=CgXMhBClEPb21eBnF24:AAGBfm0AAAAAYBliD263ZD8jvgxzmFueC9n3q46yjXSa&scisig=AAGBfm0AAAAAYBliD6ssQ0q2W81X9UTY_wGjfqNES_Mq&scisf=4&ct=citation&cd=-1&hl=en)


## Understanding the Origins of Bias in Word Embeddings

Paper on bias in word embeddings which presents a way to identify (and remove) documents whose removal most reduces bias. 

[Link to PDF](https://arxiv.org/pdf/1810.03611.pdf) | [BibTeX Entry](https://scholar.googleusercontent.com/scholar.bib?q=info:bRx57gSkp_oJ:scholar.google.com/&output=citation&scisdr=CgXMhBClEPb21eBrHS8:AAGBfm0AAAAAYBluBS-S2lZJ_wcjIKg2xa7DB5Qi6b2b&scisig=AAGBfm0AAAAAYBluBaS2tgi3or0zb2-05Ofv8VrPeRBG&scisf=4&ct=citation&cd=-1&hl=en)


## Measuring Gender Bias in Word Embeddings across Domains and Discovering New Gender Bias Word Categories

A paper which proposes an algorithm to discover new word categories within the WEAT framework. [GitHub repo](https://github.com/alfredomg/GeBNLP2019)

[Link to PDF](https://www.aclweb.org/anthology/W19-3804.pdf) | [BibTeX Entry](https://scholar.googleusercontent.com/scholar.bib?q=info:S5stJ0wV2RQJ:scholar.google.com/&output=citation&scisdr=CgXMhBClEPb21eB-0ZE:AAGBfm0AAAAAYBl7yZHFsSr5FQGepah683GVj7uQNXLL&scisig=AAGBfm0AAAAAYBl7yW2AeVjAgp_sUktuV2uYs03r5EEi&scisf=4&ct=citation&cd=-1&hl=en)


## Semantics derived automatically from language corpora contain human-like biases

This is the original paper to introduce the **Word Embedding Association Test (WEAT)**.

[Link to PDF](https://researchportal.bath.ac.uk/en/publications/semantics-derived-automatically-from-language-corpora-necessarily) | [BibTeX Entry](https://scholar.googleusercontent.com/scholar.bib?q=info:Is459GpUm20J:scholar.google.com/&output=citation&scisdr=CgXMhBClEPb21eBxgiA:AAGBfm0AAAAAYBl0miDk7C_jkbmunCFeFAt4y31PvtBz&scisig=AAGBfm0AAAAAYBl0muqLuVrhmKoLPIvFKeXxWFLMqwoM&scisf=4&ct=citation&cd=-1&hl=en)



## Studying Political Bias via Word Embeddings

[Link to PDF](https://people.clarkson.edu/~jmatthew/publications/PoliticalBias_FATES2020.pdf) | [BibTeX Entry](https://scholar.googleusercontent.com/scholar.bib?q=info:hCjFOKweqQoJ:scholar.google.com/&output=citation&scisdr=CgXMhBClEPb21eB4N9Q:AAGBfm0AAAAAYBl9L9RcGPoEb9KnrvFMNx93BO-wRDeV&scisig=AAGBfm0AAAAAYBl9L3mNqtGCZEWXN2w911ATeYbwCfRv&scisf=4&ct=citation&cd=-1&hl=en)


## Disembodied Machine Learning: On the Illusion of Objectivity in NLP

https://openreview.net/pdf?id=fkAxTMzy3fs

## Stance Detection with Bidirectional Conditional Encoding

by Augenstein and Rocktaeschel et al

[Link to PDF](https://arxiv.org/pdf/1606.05464.pdf) | [BibTeX Entry](https://scholar.googleusercontent.com/scholar.bib?q=info:WjTPTWBJOTMJ:scholar.google.com/&output=citation&scisdr=CgXMhBClEPb21eB7fBE:AAGBfm0AAAAAYBl-ZBHYOTZITGZrggoPKA7zdQFyk_QM&scisig=AAGBfm0AAAAAYBl-ZALutT4xHXQmJJZ41z4LWHEhctr8&scisf=4&ct=citation&cd=-1&hl=en)






## Google Blog Entries

 - [Text Embedding Models Contain Bias. Here's Why That Matters.](https://developers.googleblog.com/2018/04/text-embedding-models-contain-bias.html), a Google team's own investigation into the WEAT and surrounding issues







