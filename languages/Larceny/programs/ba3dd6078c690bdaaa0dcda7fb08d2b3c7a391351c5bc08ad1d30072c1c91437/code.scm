;;; Factorial computation in Larceny Scheme
;;; Demonstrates recursive factorial function

(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(define (main)
  (display "Factorial of 5: ")
  (display (factorial 5))
  (newline)
  (display "Factorial of 10: ")
  (display (factorial 10))
  (newline))

(main)
