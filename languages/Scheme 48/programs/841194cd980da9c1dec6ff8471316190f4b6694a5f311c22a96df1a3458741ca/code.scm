(define (fibonacci n)
  (if (<= n 1)
      n
      (+ (fibonacci (- n 1))
         (fibonacci (- n 2)))))

(define (main)
  (display "Fibonacci sequence:")
  (newline)
  (do ((i 0 (+ i 1)))
      ((= i 15))
    (display i)
    (display ": ")
    (display (fibonacci i))
    (newline)))

(main)