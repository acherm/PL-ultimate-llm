;;; Factorial function in Lisp
;;; Demonstrates recursion and conditional logic

(defun factorial (n)
  "Compute the factorial of N"
  (cond ((zerop n) 1)
        ((< n 0) (error "Factorial not defined for negative numbers"))
        (t (* n (factorial (- n 1))))))

;;; Test the function
(print (factorial 0))  ; Should print 1
(print (factorial 5))  ; Should print 120
(print (factorial 10)) ; Should print 3628800
