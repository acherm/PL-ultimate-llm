(define (factorial n)
  (cond
    ((= n 0) 1)
    (else (* n (factorial (- n 1))))))

(define (main)
  (print (factorial 5))
  (newline))

(main)
