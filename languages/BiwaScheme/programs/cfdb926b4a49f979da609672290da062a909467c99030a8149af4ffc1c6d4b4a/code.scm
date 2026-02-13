(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(define (print-factorials n)
  (define (iter i)
    (when (<= i n)
      (display i)
      (display "! = ")
      (display (factorial i))
      (newline)
      (iter (+ i 1))))
  (iter 1))

(print-factorials 10)
