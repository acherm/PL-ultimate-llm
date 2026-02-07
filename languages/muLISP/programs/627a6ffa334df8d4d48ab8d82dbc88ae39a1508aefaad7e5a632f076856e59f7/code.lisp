; Factorial function in muLISP
(defun factorial (n)
  (if (zerop n)
      1
      (* n (factorial (- n 1)))))

; Test the function
(print (factorial 5))
(print (factorial 10))