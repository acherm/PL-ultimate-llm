(DEFINEQ (FACTORIAL (N)
  (COND
    ((ZEROP N) 1)
    (T (TIMES N (FACTORIAL (SUB1 N)))))))

(PRINTOUT "Factorial of 5 is: " (FACTORIAL 5) T)
