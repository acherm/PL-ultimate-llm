(defun fibonacci (n)
  "Calculate the nth Fibonacci number"
  (cond
    ((<= n 0) 0)
    ((= n 1) 1)
    (t (+ (fibonacci (- n 1))
          (fibonacci (- n 2))))))

(defun print-fibonacci (count)
  "Print the first count Fibonacci numbers"
  (dotimes (i count)
    (format t "F(~D) = ~D~%" i (fibonacci i))))

(print-fibonacci 10)
