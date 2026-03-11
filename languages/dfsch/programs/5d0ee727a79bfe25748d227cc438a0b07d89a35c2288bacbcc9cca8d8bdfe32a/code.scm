;;; Fibonacci and factorial in dfsch

(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(define (fib n)
  (cond ((= n 0) 0)
        ((= n 1) 1)
        (else (+ (fib (- n 1)) (fib (- n 2))))))

(display "Factorials:")
(newline)
(do ((i 1 (+ i 1)))
    ((> i 10))
  (display (factorial i))
  (newline))

(display "Fibonacci:")
(newline)
(do ((i 0 (+ i 1)))
    ((= i 10))
  (display (fib i))
  (newline))
