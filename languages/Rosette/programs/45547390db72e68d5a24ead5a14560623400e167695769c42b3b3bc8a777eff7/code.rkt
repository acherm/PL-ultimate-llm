#lang rosette

(require rosette/lib/synthax)

; Define a symbolic integer
(define-symbolic x integer?)

; Add constraint: x^2 = 16
(solve
 (begin
   (assert (= (* x x) 16))
   x))
