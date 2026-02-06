(define (fib n)
  (if (<= n 1)
      n
      (+ (fib (- n 1))
         (fib (- n 2)))))

(define (main)
  (let loop ((i 0))
    (if (< i 10)
        (begin
          (display (fib i))
          (newline)
          (loop (+ i 1))))))

(main)
