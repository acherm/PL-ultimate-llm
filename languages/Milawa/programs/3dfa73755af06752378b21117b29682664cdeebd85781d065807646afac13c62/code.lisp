;;; Milawa: append function definition and proof
;;; From the Milawa theorem prover (Jared Davis, UT Austin)

(%defun app (x y)
  (if (consp x)
      (cons (car x) (app (cdr x) y))
    y))

(%prove (%theorem app-of-nil
  (equal (app nil y) y)))
(%auto)
(%qed)

(%prove (%theorem consp-of-app
  (equal (consp (app x y))
         (if (consp x)
             t
           (consp y)))))
(%induct (len x))
(%auto)
(%qed)
