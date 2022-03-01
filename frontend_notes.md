# Questions/Remarks

 - if a certain object parameter is used for search (e.g. Department=Afrika), should that parameter (=Department) 
 temporarily be removed as an x-axis sorting variable? (since all points will have the same position)  
  => can be done backend  
  => removing might cause confusion, not taking action
  

 - should the /examples route be /examples/{datasetID}?
   => no, so that examples from different datasets can be shown

 - is selection of multiple items useful? if so, what would that do/imply?  ]
   -> might be good for (min, avg, max) and bias score indicators  
   -> more of a point for discussion & for future work  
   => skip for now

 - normalisation: what normalising function does the frontend apply?  
   -> especially on the indicator scores  
   -> I've noticed that it might be easier if the backend makes sure that scores are normalised and the
      front-end assumes that values are always in the range [0, 1] (or [0, 100] equivalently) and cuts off anything
      outside of range (this could also be done by the backend); reason I say this is because normalisation turned
      out even more intricate than I expected  
   => add median, but not now
   => front-end shouldn't do normalisation -> let Werner know if this is the case    
   => front-end takes indicator scores literally -> shouldn't do anything to those 

# Improvements

 - shown value markers on the x-axis, especially if x is a categorical variable (e.g. for Department it's not clear
   what each of the vertical columns represents); similarly with dates, it would be helpful to have a few markers  
   => Werner will experiment a bit
   
 - about {avg, min, max}: I really like the idea but:
    - change order to {min, avg, max}  
    - I apply normalisation so that min is always 0 and max is always 100, making these a bit pointless     
      -> data also doesn't have many "gaps" wrt the scores, so even if min_score and max_score params are used  
         the reported min and max values be almost exactly be the params' values  
      -> could think about other descriptive stats to put there, like standard deviation or something
         about the indicator values 
    => order will be changed  
    => min and max really are still useful for zooming in and out   




# Issues

 - object cards (appear when hovering points) don't bounce off the bottom of the window (on Firefox on Linux)  
   => will be fixed

 - static field description given by backend not used by frontend?  
   => wrong in the backend

 - "evidence" (i.e. score details/score indicators) can also be words in the title (only word in description
   are highlighted)  
   => will be fixed

 - keywords, when added by clicking on words in the score detail list, should be COMMA-separated 
   (currently separated by space): I want people to be able to search multiword expressions  
   => will be fixed  
   =>  description, make examples with comma-separated keywords
