#!/usr/bin/env guile
!#

;;; Factorial and Fibonacci in GNU Guile

(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(define (fib n)
  (let loop ((i n) (a 0) (b 1))
    (if (zero? i)
        a
        (loop (- i 1) b (+ a b)))))

(display "Factorials 0..10:")
(newline)
(let loop ((i 0))
  (when (<= i 10)
    (format #t "  ~a! = ~a~%" i (factorial i))
    (loop (+ i 1))))

(newline)
(display "Fibonacci 0..14:")
(newline)
(let loop ((i 0))
  (when (< i 15)
    (format #t "  fib(~a) = ~a~%" i (fib i))
    (loop (+ i 1))))
