::  Fibonacci sequence
|=  n=@ud
=|  [i=@ud t=@ud]
|-  ^-  @ud
?:  =(n 0)  0
?:  =(n 1)  1
=.  i  1
|-  ^-  @ud
?:  =(n 2)  (add i t)
$(n (dec n), i (add i t), t i)