(define (fib n)
  (if (< n 2)
      n
      (+ (fib (- n 1)) (fib (- n 2)))))

(do ((i 0 (+ i 1)))
    ((= i 10))
  (display (fib i))
  (newline))
