;;; Fibonacci sequence generator in CLISP
;;; Computes the nth Fibonacci number recursively

(defun fib (n)
  "Compute the nth Fibonacci number"
  (cond
    ((= n 0) 0)
    ((= n 1) 1)
    (t (+ (fib (- n 1)) (fib (- n 2))))))

(defun print-fib-sequence (count)
  "Print the first count Fibonacci numbers"
  (dotimes (i count)
    (format t "fib(~a) = ~a~%" i (fib i))))

;; Example: Print first 10 Fibonacci numbers
(print-fib-sequence 10)