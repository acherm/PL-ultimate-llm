(defun factorial (n)
  (cond ((zerop n) 1)
        (t (times n (factorial (difference n 1))))))

(print (factorial 5))
