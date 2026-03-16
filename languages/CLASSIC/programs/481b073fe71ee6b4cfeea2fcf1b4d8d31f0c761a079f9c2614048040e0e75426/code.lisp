;; CLASSIC description logic example: simple family ontology

(define-concept Person (primitive Top))

(define-concept Female (primitive Person))

(define-concept Male (primitive Person))

(define-concept Parent
  (and Person
       (at-least 1 has-child Person)))

(define-concept Mother
  (and Female Parent))

(define-concept Father
  (and Male Parent))

(define-individual MARY
  :instance-of Female
  :fills (has-child JOHN))

(define-individual JOHN
  :instance-of Male)
