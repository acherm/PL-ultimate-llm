(defun factorial (n)
  "Calculate factorial of n"
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(format t "Factorial of 5: ~a~%" (factorial 5))
(format t "Factorial of 10: ~a~%" (factorial 10))
