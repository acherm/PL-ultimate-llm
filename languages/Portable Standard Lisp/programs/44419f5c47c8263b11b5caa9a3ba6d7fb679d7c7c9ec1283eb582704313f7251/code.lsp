% Factorial function in Portable Standard Lisp (PSL)

(de factorial (n)
  (cond
    ((equal n 0) 1)
    ((equal n 1) 1)
    (t (times n (factorial (difference n 1))))))

% Test the factorial function
(prin2 "Factorial of 5: ")
(prin2 (factorial 5))
(terpri)

(prin2 "Factorial of 10: ")
(prin2 (factorial 10))
(terpri)
