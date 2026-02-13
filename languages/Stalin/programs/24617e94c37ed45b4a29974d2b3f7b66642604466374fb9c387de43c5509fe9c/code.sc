(define (tak x y z)
 (if (not (< y x))
     z
     (tak (tak (- x 1) y z) (tak (- y 1) z x) (tak (- z 1) x y))))

(do ((i 0 (+ i 1))) ((= i 1000))
 (write (tak 18 12 6))
 (newline))
