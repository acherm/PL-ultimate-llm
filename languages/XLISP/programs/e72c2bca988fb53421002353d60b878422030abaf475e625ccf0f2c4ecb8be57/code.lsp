;;; Factorial function in XLISP
;;; Computes factorial using recursion

(defun factorial (n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

;; Test the function
(print (factorial 5))
(print (factorial 10))