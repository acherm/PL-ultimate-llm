(defun fact (n)
  (if (zp n)
      1
      (* n (fact (1- n)))))