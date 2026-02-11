;;; Fibonacci number calculator
;;; Demonstrates recursive and iterative approaches

(defun fib-recursive (n)
  "Calculate Fibonacci number recursively"
  (cond
    ((<= n 0) 0)
    ((= n 1) 1)
    (t (+ (fib-recursive (- n 1))
          (fib-recursive (- n 2))))))

(defun fib-iterative (n)
  "Calculate Fibonacci number iteratively"
  (if (<= n 0)
      0
      (loop for i from 1 to n
            for a = 0 then b
            for b = 1 then (+ a b)
            finally (return a))))

(defun main ()
  "Demonstrate both Fibonacci implementations"
  (format t "Fibonacci numbers (recursive):~%")
  (loop for i from 0 to 10
        do (format t "  fib(~D) = ~D~%" i (fib-recursive i)))
  (format t "~%Fibonacci numbers (iterative):~%")
  (loop for i from 0 to 20
        do (format t "  fib(~D) = ~D~%" i (fib-iterative i))))

(main)
