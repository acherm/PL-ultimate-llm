(defun bottles (n)
  (if (zerop n) "no more bottles"
      (format nil "~:*~r bottle~:p of beer" n)))

(defun verse (n)
  (format nil "~a on the wall, ~a.~%~a one down, pass it around, ~a on the wall.~%~%"
          (bottles n) (bottles n) (if (zerop n) "Go to the store and buy some more" (bottles (1- n))) (bottles (1- n))))

(do ((i 99 (1- i))) ((zerop i)) (princ (verse i)))