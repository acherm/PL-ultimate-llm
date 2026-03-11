; Hello World and Fibonacci in ChrysaLisp
(print "Hello, World!")

(defun fib (n)
	(if (< n 2) n
		(+ (fib (- n 1)) (fib (- n 2)))))

(each (range 0 10) (lambda (n)
	(print (cat "fib(" (str n 10) ") = " (str (fib n) 10)))))
