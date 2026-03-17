;;; Fibonacci sequence in S-1 Lisp
;;; S-1 Lisp was a Lisp dialect developed at Lawrence Livermore National Laboratory
;;; for the S-1 Mark IIA supercomputer, circa 1982.

(defun fibonacci (n)
  (cond ((zerop n) 0)
        ((= n 1) 1)
        (t (+ (fibonacci (- n 1))
              (fibonacci (- n 2))))))

(defun print-fibs (limit)
  (do ((i 0 (+ i 1)))
      ((= i limit))
    (print (fibonacci i))
    (terpri)))

(print-fibs 10)
