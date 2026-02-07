(module fibonacci
   (main main))

(define (fib n)
   (if (<= n 1)
       n
       (+ (fib (- n 1)) (fib (- n 2)))))

(define (main args)
   (let ((n 10))
      (print "Fibonacci sequence up to " n ":")
      (do ((i 0 (+ i 1)))
          ((> i n))
         (print "fib(" i ") = " (fib i)))))
