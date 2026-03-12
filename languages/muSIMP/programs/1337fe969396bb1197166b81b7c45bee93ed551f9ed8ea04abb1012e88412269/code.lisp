;; muSIMP: Recursive factorial and Fibonacci
;; muSIMP is a simplified Lisp dialect by Soft Warehouse (Stoutemyer & Rich)

(PROCEDURE FACT (N)
  (COND ((EQ N 0) 1)
        (T (TIMES N (FACT (DIFFERENCE N 1))))))

(PROCEDURE FIB (N)
  (COND ((LEQ N 1) N)
        (T (PLUS (FIB (DIFFERENCE N 1))
                 (FIB (DIFFERENCE N 2))))))

(PRINT (FACT 10))
(PRINT (FIB 10))
