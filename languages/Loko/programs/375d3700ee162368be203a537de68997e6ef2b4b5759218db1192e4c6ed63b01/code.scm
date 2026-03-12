; Fibonacci sequence in Loko Scheme (R7RS)
(import (scheme base)
        (scheme write))

(define (fibonacci n)
  (let loop ((a 0) (b 1) (count n))
    (if (= count 0)
        a
        (loop b (+ a b) (- count 1)))))

(let loop ((i 0))
  (when (< i 10)
    (display (fibonacci i))
    (newline)
    (loop (+ i 1))))
