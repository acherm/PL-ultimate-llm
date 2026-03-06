;;; Micro-Planner blocks world example
;;; From: Sussman, Winograd, Charniak - Micro-planner Reference Manual, AIM-203 (1970)

;;; Assert initial state
(THASSERT (ON A B))
(THASSERT (ON B TABLE))
(THASSERT (ON C TABLE))
(THASSERT (CLEARTOP A))
(THASSERT (CLEARTOP C))

;;; Antecedent theorem: whenever X is placed ON Y, assert Y SUPPORTS X
(THANTE (#:X #:Y) (ON #:X #:Y)
  (THASSERT (SUPPORTS #:Y #:X)))

;;; Consequent theorem: ABOVE(X,Y) holds if X is directly ON Y,
;;; or X is ON some Z that is ABOVE Y
(THCONSE (#:X #:Y) (ABOVE #:X #:Y)
  (THOR
    (THGOAL (ON #:X #:Y))
    (THAND
      (THGOAL (ON #:X #:Z))
      (THGOAL (ABOVE #:Z #:Y)))))

;;; Query: is A above TABLE?
(THGOAL (ABOVE A TABLE))
