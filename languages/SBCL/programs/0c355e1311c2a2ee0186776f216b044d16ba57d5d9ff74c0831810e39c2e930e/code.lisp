(defun factorial (n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(defun main ()
  (format t "Factorial of 5: ~d~%" (factorial 5))
  (format t "Factorial of 10: ~d~%" (factorial 10)))

(main)