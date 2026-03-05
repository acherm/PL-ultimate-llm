#lang racket
(require cKanren)

;; Find all pairs (x y) from {1 2 3} where x != y
;; demonstrating cKanren's disequality constraint =/=

(define pairs
  (run* (q)
    (fresh (x y)
      (membero x '(1 2 3))
      (membero y '(1 2 3))
      (=/= x y)
      (== q `(,x ,y)))))

(for-each displayln pairs)
