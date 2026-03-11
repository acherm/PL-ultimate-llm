;;; Fibonacci sequence implementation for Movitz
;;; Movitz is a Common Lisp implementation for bare x86 hardware

(defun fibonacci (n)
  "Compute the nth Fibonacci number recursively."
  (cond ((= n 0) 0)
        ((= n 1) 1)
        (t (+ (fibonacci (- n 1))
              (fibonacci (- n 2))))))

(defun print-fibonacci (count)
  "Print the first COUNT Fibonacci numbers."
  (dotimes (i count)
    (format t "F(~d) = ~d~%" i (fibonacci i))))

(print-fibonacci 10)
