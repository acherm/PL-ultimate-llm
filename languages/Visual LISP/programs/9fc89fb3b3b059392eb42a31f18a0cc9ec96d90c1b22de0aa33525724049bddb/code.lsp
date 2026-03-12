; Fibonacci sequence in Visual LISP (AutoLISP)
; Iterative implementation

(defun fibonacci (n / a b tmp)
  (setq a 0  b 1)
  (repeat n
    (setq tmp b
          b   (+ a b)
          a   tmp))
  a)

(defun c:FIBTEST ( / i)
  (setq i 0)
  (while (< i 10)
    (princ (strcat "\nfib(" (itoa i) ") = " (itoa (fibonacci i))))
    (setq i (1+ i)))
  (princ))
