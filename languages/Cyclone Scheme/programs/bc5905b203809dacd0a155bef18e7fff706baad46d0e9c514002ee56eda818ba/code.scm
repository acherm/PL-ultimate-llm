;; Fibonacci sequence using Cyclone Scheme (R7RS)
(import (scheme base)
        (scheme write))

(define (fib n)
  (cond
    ((= n 0) 0)
    ((= n 1) 1)
    (else (+ (fib (- n 1)) (fib (- n 2))))))

(display "Fibonacci sequence:")
(newline)
(let loop ((i 0))
  (when (< i 10)
    (display (fib i))
    (display " ")
    (loop (+ i 1))))
(newline)
