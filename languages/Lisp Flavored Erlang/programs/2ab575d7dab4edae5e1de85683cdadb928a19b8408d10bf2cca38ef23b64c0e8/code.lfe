(defmodule fibonacci
  (export (fib 1) (main 0)))

(defun fib
  ((0) 0)
  ((1) 1)
  ((n) (+ (fib (- n 1)) (fib (- n 2)))))

(defun main ()
  (lists:foreach
    (lambda (n)
      (io:format "fib(~p) = ~p~n" (list n (fib n))))
    (lists:seq 0 10)))
