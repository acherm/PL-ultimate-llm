(defmodule fibonacci
  (export (fib 1) (main 0)))

(defun fib
  ((0) 0)
  ((1) 1)
  ((n) (+ (fib (- n 1)) (fib (- n 2)))))

(defun main ()
  (let ((results (lists:map #'fib/1 (lists:seq 0 10))))
    (io:format "Fibonacci(0..10): ~p~n" (list results))))
