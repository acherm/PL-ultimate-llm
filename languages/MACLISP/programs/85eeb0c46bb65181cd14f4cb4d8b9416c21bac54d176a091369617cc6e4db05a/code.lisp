;;; Factorial function in MACLISP

(defun factorial (n)
  (cond ((zerop n) 1)
        (t (times n (factorial (sub1 n))))))

;;; Example usage
(factorial 5)
