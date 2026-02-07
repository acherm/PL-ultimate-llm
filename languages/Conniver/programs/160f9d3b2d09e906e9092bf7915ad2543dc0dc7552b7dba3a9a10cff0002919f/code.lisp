; Conniver pattern matching example
; Append two lists
(DEFINE (APPEND L1 L2)
  (COND ((NULL L1) L2)
        (T (CONS (CAR L1)
                 (APPEND (CDR L1) L2)))))

; Test
(APPEND '(A B C) '(D E F))
