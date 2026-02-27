; Fibonacci numbers in Otus Lisp
; Otus Lisp is an R7RS-compatible Scheme dialect

(define (fib n)
   (let loop ((n n) (a 0) (b 1))
      (if (= n 0)
         a
         (loop (- n 1) b (+ a b)))))

(for-each
   (lambda (n)
      (display "fib(")
      (display n)
      (display ") = ")
      (display (fib n))
      (newline))
   '(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15))
