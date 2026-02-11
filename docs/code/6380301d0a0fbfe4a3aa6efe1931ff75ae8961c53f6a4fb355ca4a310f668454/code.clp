(deftemplate factorial
   (slot n)
   (slot result))

(defrule calculate-factorial
   ?f <- (factorial (n ?n) (result nil))
   (test (> ?n 0))
   =>
   (bind ?fact 1)
   (bind ?i ?n)
   (while (> ?i 0)
      (bind ?fact (* ?fact ?i))
      (bind ?i (- ?i 1)))
   (modify ?f (result ?fact)))

(defrule print-result
   (factorial (n ?n) (result ?result))
   (test (neq ?result nil))
   =>
   (printout t "Factorial of " ?n " is " ?result crlf))

(deffacts startup
   (factorial (n 5) (result nil))
   (factorial (n 10) (result nil)))

(reset)
(run)
