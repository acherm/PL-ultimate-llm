(for i 1 100
  (prn
    (aif (and (is 0 i % 15) "FizzBuzz")
         it
      (aif (and (is 0 i % 5) "Buzz")
           it
        (aif (and (is 0 i % 3) "Fizz")
             it
           i)))))