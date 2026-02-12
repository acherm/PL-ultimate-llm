(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(display "Factorial of 5: ")
(display (factorial 5))
(newline)

(define (fibonacci n)
  (cond
    ((<= n 0) 0)
    ((= n 1) 1)
    (else (+ (fibonacci (- n 1)) (fibonacci (- n 2))))))

(display "Fibonacci of 10: ")
(display (fibonacci 10))
(newline)