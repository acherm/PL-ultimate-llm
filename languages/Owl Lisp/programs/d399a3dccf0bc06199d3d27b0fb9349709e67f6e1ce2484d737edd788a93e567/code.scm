;; Factorial function in Owl Lisp
(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

;; Print factorial of 10
(print (factorial 10))