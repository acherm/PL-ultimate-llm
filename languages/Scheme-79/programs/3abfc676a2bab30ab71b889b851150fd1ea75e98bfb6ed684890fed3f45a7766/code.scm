; Factorial function in Scheme
(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

; Compute factorial of 5
(factorial 5)
