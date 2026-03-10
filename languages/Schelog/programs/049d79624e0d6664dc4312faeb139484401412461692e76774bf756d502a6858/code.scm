#lang racket
(require schelog)

; Family facts
(define %parent
  (extend-relation (a b)
    (fact () 'tom 'bob)
    (fact () 'tom 'liz)
    (fact () 'bob 'ann)
    (fact () 'bob 'pat)))

; Grandparent rule derived from parent
(define %grandparent
  (extend-relation (a b)
    (rule (a b) (c)
      (%parent a c)
      (%parent c b))))

; Query: who are tom's grandchildren?
(define grandchildren
  (run* (q)
    (%grandparent 'tom q)))

(displayln "Tom's grandchildren:")
(for-each displayln grandchildren)
