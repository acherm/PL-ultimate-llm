(import (rnrs))

(define (fib n)
  (let loop ((i 0) (a 0) (b 1))
    (if (= i n)
        a
        (loop (+ i 1) b (+ a b)))))

(for-each
  (lambda (n)
    (display n)
    (display ": ")
    (display (fib n))
    (newline))
  (list 0 1 2 3 4 5 6 7 8 9 10))
