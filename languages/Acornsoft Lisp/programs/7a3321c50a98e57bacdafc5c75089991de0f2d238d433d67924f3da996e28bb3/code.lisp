(defun factorial (n)
  (cond ((zerop n) 1)
        (t (times n (factorial (sub1 n))))))

(defun factorial (n (result . 1))
  (loop
    (until (zerop n) result)
    (setq result (times n result))
    (setq n (sub1 n))))
