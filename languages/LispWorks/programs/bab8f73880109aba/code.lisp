;;; Fibonacci sequence generator
;;; Simple recursive implementation

(defun fibonacci (n)
  "Calculate the nth Fibonacci number"
  (cond
    ((<= n 0) 0)
    ((= n 1) 1)
    (t (+ (fibonacci (- n 1))
          (fibonacci (- n 2))))))

;;; Test the function
(format t "Fibonacci sequence:~%")
(dotimes (i 10)
  (format t "F(~d) = ~d~%" i (fibonacci i)))
