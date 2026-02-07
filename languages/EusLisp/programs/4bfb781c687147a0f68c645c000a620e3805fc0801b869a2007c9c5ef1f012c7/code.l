;;; Factorial function in EusLisp
(defun factorial (n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

;;; Calculate and print factorials
(dotimes (i 10)
  (format t "~d! = ~d~%" i (factorial i)))