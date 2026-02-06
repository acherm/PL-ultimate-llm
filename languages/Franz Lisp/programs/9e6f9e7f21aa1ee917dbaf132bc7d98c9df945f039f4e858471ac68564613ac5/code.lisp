(defun factorial (n)
  (cond ((= n 0) 1)
        (t (* n (factorial (- n 1))))))

(print (factorial 5))
(print (factorial 10))