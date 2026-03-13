(import (scheme base)
        (scheme write))

(define (fib n)
  (let loop ((i n) (a 0) (b 1))
    (if (= i 0)
        a
        (loop (- i 1) b (+ a b)))))

(define (show-fibs limit)
  (let loop ((i 0))
    (when (<= i limit)
      (display "fib(")
      (display i)
      (display ") = ")
      (display (fib i))
      (newline)
      (loop (+ i 1)))))

(show-fibs 15)
