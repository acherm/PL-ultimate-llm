#lang cur

(define-type Nat
  (data
    [z : Nat]
    [s : (-> Nat Nat)]))

(define-term plus : (-> Nat (-> Nat Nat))
  (lambda (m n)
    (elim Nat
      (lambda (_) Nat)
      n
      (lambda (_ ih) (s ih))
      m)))

(define-term two : Nat
  (s (s z)))

(define-term four : Nat
  (plus two two))
