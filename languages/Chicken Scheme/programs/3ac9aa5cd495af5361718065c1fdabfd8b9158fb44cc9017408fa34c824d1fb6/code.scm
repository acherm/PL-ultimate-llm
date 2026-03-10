(define (fib n)
  (let loop ((i n) (a 0) (b 1))
    (if (zero? i)
        a
        (loop (- i 1) b (+ a b)))))

(do ((i 0 (+ i 1)))
    ((= i 16))
  (display (fib i))
  (newline))
