(import (owl base))

(define (fib n)
   (cond
      ((= n 0) 0)
      ((= n 1) 1)
      (else (+ (fib (- n 1)) (fib (- n 2))))))

(for-each
   (lambda (n)
      (print (fib n)))
   (iota 10 0 1))
