;; Fibonacci sequence in Embeddable Common Lisp (ECL)
(defun fibonacci (n)
  (if (< n 2)
      n
      (+ (fibonacci (- n 1))
         (fibonacci (- n 2)))))

(defun print-fibs (limit)
  (loop for i from 0 to limit
        do (format t "fib(~a) = ~a~%" i (fibonacci i))))

(print-fibs 10)
