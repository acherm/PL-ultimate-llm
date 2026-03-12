(clear-all)

(define-model count

  (sgp :v t)

  (chunk-type count-order first second)
  (chunk-type count-from start end count)

  (add-dm
   (b isa count-order first 1 second 2)
   (c isa count-order first 2 second 3)
   (d isa count-order first 3 second 4)
   (e isa count-order first 4 second 5)
   (f isa count-order first 5 second 6)
   (first-goal isa count-from start 2 end 4))

  (goal-focus first-goal)

  (p start
    =goal>
    isa count-from
    start =num1
    count nil
   ==>
    =goal>
    count =num1
    +retrieval>
    isa count-order
    first =num1)

  (p increment
    =goal>
    isa count-from
    count =num1
    =retrieval>
    isa count-order
    first =num1
    second =num2
   ==>
    =goal>
    count =num2
    +retrieval>
    isa count-order
    first =num2)

  (p stop
    =goal>
    isa count-from
    end =num
    count =num
   ==>
    -goal>))
