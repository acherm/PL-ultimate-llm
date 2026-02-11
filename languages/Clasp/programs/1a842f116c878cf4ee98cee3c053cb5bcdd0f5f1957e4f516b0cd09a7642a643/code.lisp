(defun fibonacci (n)
  "Calculate the nth Fibonacci number recursively"
  (cond
    ((<= n 0) 0)
    ((= n 1) 1)
    (t (+ (fibonacci (- n 1))
          (fibonacci (- n 2))))))

(defun print-fibonacci-sequence (count)
  "Print the first count Fibonacci numbers"
  (dotimes (i count)
    (format t "F(~d) = ~d~%" i (fibonacci i))))

;; Print first 10 Fibonacci numbers
(print-fibonacci-sequence 10)
