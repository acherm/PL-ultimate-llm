#!/usr/bin/env vicare
;; Factorial calculator using tail recursion
(import (vicare))

(define (factorial n)
  (let loop ((i n) (acc 1))
    (if (<= i 1)
        acc
        (loop (- i 1) (* acc i)))))

(define (main)
  (display "Enter a number: ")
  (flush-output-port (current-output-port))
  (let ((n (read)))
    (if (and (integer? n) (>= n 0))
        (begin
          (display "Factorial of ")
          (display n)
          (display " is ")
          (display (factorial n))
          (newline))
        (begin
          (display "Please enter a non-negative integer.")
          (newline)))))

(main)