(DEFINEQ
  (FACTORIAL
    (LAMBDA (N)
      (COND
        ((ZEROP N) 1)
        (T (ITIMES N (FACTORIAL (SUB1 N))))))))

(DEFINEQ
  (FIB
    (LAMBDA (N)
      (COND
        ((EQ N 0) 0)
        ((EQ N 1) 1)
        (T (IPLUS (FIB (SUB1 N))
                  (FIB (IDIFFERENCE N 2))))))))

(PRINT (FACTORIAL 10))
(PRINT (FIB 10))
