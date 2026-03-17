; Factorial function in LSharp (L#)
; A Lisp dialect for the .NET CLR

(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(display "Factorial examples:")
(newline)
(let loop ((i 1))
  (when (<= i 10)
    (display i)
    (display "! = ")
    (display (factorial i))
    (newline)
    (loop (+ i 1))))
