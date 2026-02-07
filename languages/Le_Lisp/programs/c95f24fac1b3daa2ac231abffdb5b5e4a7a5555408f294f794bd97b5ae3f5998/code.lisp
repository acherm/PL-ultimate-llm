;;; Factorial function in Le_Lisp
(defun factorial (n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

;;; Test the factorial function
(print (factorial 5))
(print (factorial 10))
