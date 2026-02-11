;;; Fibonacci sequence generator in Elk Scheme
(define (fibonacci n)
  (cond ((= n 0) 0)
        ((= n 1) 1)
        (else (+ (fibonacci (- n 1))
                 (fibonacci (- n 2))))))

(define (print-fibonacci count)
  (do ((i 0 (+ i 1)))
      ((>= i count))
    (display "fib(")
    (display i)
    (display ") = ")
    (display (fibonacci i))
    (newline)))

(print-fibonacci 10)
