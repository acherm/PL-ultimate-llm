;; Factorial function using tail recursion
(define (factorial n)
  (define (fact-iter product counter max-count)
    (if (> counter max-count)
        product
        (fact-iter (* counter product)
                   (+ counter 1)
                   max-count)))
  (fact-iter 1 1 n))

;; Test the factorial function
(display "Factorial of 5: ")
(display (factorial 5))
(newline)

(display "Factorial of 10: ")
(display (factorial 10))
(newline)
