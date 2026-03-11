; Fibonacci sequence in Forsp
; A stack-based language combining Forth and Lisp

(def fib
  (dup 2 lt
    ()
    (dup 1 - fib
     swap 2 - fib
     +)
    cond))

0 fib print
1 fib print
2 fib print
3 fib print
4 fib print
5 fib print
6 fib print
7 fib print
