;;; Kanren: relational list append
;;; Demonstrates the core of Kanren's logic programming model.

(load "kanren.scm")

;; The appendo relation: l and s concatenated give out
(define appendo
  (lambda (l s out)
    (conde
      ((== '() l) (== s out))
      ((fresh (a d res)
         (conso a d l)
         (conso a res out)
         (appendo d s res))))))

;; Forward: append two known lists
(display (run 1 (q) (appendo '(a b c) '(d e) q)))
(newline)
;; => ((a b c d e))

;; Backward: enumerate all ways to split a list
(display
  (run* (q)
    (fresh (x y)
      (== q (list x y))
      (appendo x y '(1 2 3)))))
(newline)
;; => ((() (1 2 3)) ((1) (2 3)) ((1 2) (3)) ((1 2 3) ()))
