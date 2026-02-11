;;; Factorial function in OpenLisp (ISLISP)
(defun factorial (n)
  "Compute the factorial of n"
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

;;; Test the factorial function
(format (standard-output) "Factorial of 5 is: ~D~%" (factorial 5))
(format (standard-output) "Factorial of 10 is: ~D~%" (factorial 10))
