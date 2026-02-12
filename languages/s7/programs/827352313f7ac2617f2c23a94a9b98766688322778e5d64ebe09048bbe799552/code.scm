;;; Factorial function in s7 Scheme
(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

;;; Test the factorial function
(display "Factorial of 5: ")
(display (factorial 5))
(newline)

(display "Factorial of 10: ")
(display (factorial 10))
(newline)
