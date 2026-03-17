; Factorial and Fibonacci in LispMe (Scheme for Palm OS)
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

(define (fib n)
  (cond ((= n 0) 0)
        ((= n 1) 1)
        (else (+ (fib (- n 1)) (fib (- n 2))))))

(display "Factorial 10: ")
(display (factorial 10))
(newline)

(display "Fibonacci 10: ")
(display (fib 10))
(newline)
