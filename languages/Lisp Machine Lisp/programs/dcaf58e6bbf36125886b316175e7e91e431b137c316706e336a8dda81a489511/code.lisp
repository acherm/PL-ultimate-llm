(defun factorial (n)
  (if (zerop n)
      1
      (* n (factorial (1- n)))))

(defun fibonacci (n)
  (cond ((= n 0) 0)
        ((= n 1) 1)
        (t (+ (fibonacci (- n 1))
              (fibonacci (- n 2))))))

(format t "~&Factorial of 5: ~D~%" (factorial 5))
(format t "~&Fibonacci of 10: ~D~%" (fibonacci 10))
