;;; Factorial computation in MIT Scheme
;;; Demonstrates tail recursion optimization

(define (factorial n)
  (define (fact-iter product counter max-count)
    (if (> counter max-count)
        product
        (fact-iter (* counter product)
                   (+ counter 1)
                   max-count)))
  (fact-iter 1 1 n))

;;; Test cases
(display "Factorial of 5: ")
(display (factorial 5))
(newline)

(display "Factorial of 10: ")
(display (factorial 10))
(newline)

(display "Factorial of 20: ")
(display (factorial 20))
(newline)
