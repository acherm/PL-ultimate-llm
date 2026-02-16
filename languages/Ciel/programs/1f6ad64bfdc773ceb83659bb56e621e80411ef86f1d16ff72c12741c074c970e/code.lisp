(defun fibonacci (n)
  "Calculate the nth Fibonacci number."
  (if (<= n 1)
      n
      (+ (fibonacci (- n 1))
         (fibonacci (- n 2)))))

(format t "Fibonacci(10) = ~a~%" (fibonacci 10))
