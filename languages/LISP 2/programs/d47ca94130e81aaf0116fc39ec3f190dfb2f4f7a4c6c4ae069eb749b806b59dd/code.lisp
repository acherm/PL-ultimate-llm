; Factorial function in LISP 2
(LAMBDA (N)
  (COND ((ZEROP N) 1)
        (T (TIMES N (FACTORIAL (SUB1 N))))))
