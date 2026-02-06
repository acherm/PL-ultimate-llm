;;; Factorial function in ZetaLisp
(defun factorial (n)
  "Compute factorial of N"
  (if (zerop n)
      1
      (* n (factorial (1- n)))))

;;; Iterative version using DO
(defun factorial-iter (n)
  "Compute factorial of N iteratively"
  (do ((i n (1- i))
       (result 1 (* result i)))
      ((zerop i) result)))

;;; Test the functions
(print (factorial 5))
(print (factorial-iter 6))
