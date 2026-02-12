#lang typed/racket

(: factorial (-> Integer Integer))
(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(: main (-> Void))
(define (main)
  (displayln (factorial 5))
  (displayln (factorial 10)))

(main)