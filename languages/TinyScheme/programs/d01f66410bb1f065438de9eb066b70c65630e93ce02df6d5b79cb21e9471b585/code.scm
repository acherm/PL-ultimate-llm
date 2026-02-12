(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

; Test the factorial function
(display (factorial 5))
(newline)
(display (factorial 10))
(newline)