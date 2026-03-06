; Fibonacci sequence in XSCHEME
(define (fibonacci n)
  (if (< n 2)
      n
      (+ (fibonacci (- n 1)) (fibonacci (- n 2)))))

(define (print-fibs count)
  (let loop ((i 0))
    (when (< i count)
      (display (fibonacci i))
      (newline)
      (loop (+ i 1)))))

(print-fibs 10)
