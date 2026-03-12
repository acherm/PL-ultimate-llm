#lang scheme

(define (fib n)
  (cond ((= n 0) 0)
        ((= n 1) 1)
        (else (+ (fib (- n 1)) (fib (- n 2))))))

(let loop ((i 0))
  (when (< i 10)
    (printf "fib(~a) = ~a\n" i (fib i))
    (loop (+ i 1))))
