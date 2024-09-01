
```

Data Structures:
 
  = Rule Object =:
  Action_Value_Precondition:                                            Prediction:    State Value Deltas
  Action   State   Preconditions (old world)                            y  x  board    score     key
           values  precondition0    precondition1    precondition2            value    delta     delta 
           excl    y  x             y  x
           score
  ((left,  (0,),  (0, 0, ' '),     (0, 1, 'x'),     (0, 2, 'u')),      (0, 0, 'x',     (0,       0))),
  ((right, (0,),  (0, -1, 'x'),    (0, 0, 'o')),                       (0, 0, 'o',     (0,       0))),
  
  The following Action_Value_Precondition:
  ((right, (0,),  (0, -1, 'x'),    (0, 0, 'o'))
  can be read: Match if there is a 'o' at the focus point, and a 'x' to the left of it, and the action is right.
  
  The following Action_Value_Precondition, Prediction:
  ((left,  (0,),  (0, 0, ' '),     (0, 1, 'x'),     (0, 2, 'u')),      (0, 0, 'x',     (0,       0))),
  can be read: Match if there is a ' ' at the focus point, 
                        and a 'x' to the right of it, 
                        and a 'u' to the right of the 'x',
                        and the action is left
                And the prediction after the action is:
                        the 'x' will appear at 0,0 relative to the focus point.
                        and there is no change to our score

  The following Action_Value_Precondition, Prediction:
  ((right, (0,), (0, -1, 'x'), (0, 0, 'f')), (0, 0, 'x', (1, 0))),
  can be read: Match if there is a 'f' at the focus point, 
                        and a 'x' to the left of it, 
                        and the action is right
                And the prediction after the action is:
                        the 'x' will appear at 0,0 relative to the focus point.
                        the first State Delta (score) will be +1
                        the first State Delta (key) will be +0
  
  
  Rule_Evidence Object Dictionary
                                 positive       negative
                                 evidence       evidence
                                 counter        counter
  { ((right, ... ))       :    ( 1,             0                ) }
  
 { ((left, (), (0, 0, ' '), (0, 1, 'x')), (0, 0, 'x', (0,))): (1,0) }    
  
  Positive Evidence, and Negative Evidence can be used to calculate:
        Frequency         = positive_count / (positive_count + negative_count)
        Confidence        = (positive_count + negative_count) / (positive_count + negative_count + 1)
        Truth_expectation = confidence * (frequency - 0.5) + 0.5

  Location:  
    xy_loc tuple (x,y) not (0,0) is top left
  
  
  State Values 
  
```