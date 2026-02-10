;;; Simple enzyme catalysis model in Little b
(include-library :biochem)

(define-complex enzyme [E])
(define-complex substrate [S])
(define-complex enzyme-substrate [E S])
(define-complex product [P])

(define-reaction binding
  E + S <=> enzyme-substrate
  :kf 1.0
  :kr 0.5)

(define-reaction catalysis
  enzyme-substrate -> E + P
  :kf 0.8)

(define-init E 10)
(define-init S 100)