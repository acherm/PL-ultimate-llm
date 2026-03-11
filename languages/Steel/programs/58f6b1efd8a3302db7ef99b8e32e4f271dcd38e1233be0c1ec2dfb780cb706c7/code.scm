;; Fibonacci sequence in Steel
(define (fib n)
  (if (< n 2)
      n
      (+ (fib (- n 1)) (fib (- n 2)))))

(define (fib-range start end)
  (if (>= start end)
      '()
      (cons (fib start) (fib-range (+ start 1) end))))

(for-each
  (lambda (n) (display n) (newline))
  (fib-range 0 10))
