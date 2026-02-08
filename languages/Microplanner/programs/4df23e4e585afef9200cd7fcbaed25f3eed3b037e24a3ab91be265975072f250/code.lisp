;; Microplanner program demonstrating basic pattern matching
;; Example from early AI research on natural language understanding

(THASSERT (ISA CLYDE ELEPHANT))
(THASSERT (ISA FRED ELEPHANT))
(THASSERT (COLOR CLYDE GRAY))

(THGOAL (ISA ?X ELEPHANT))
;; Will bind ?X to CLYDE or FRED

(THGOAL (AND (ISA ?Y ELEPHANT) (COLOR ?Y GRAY)))
;; Will bind ?Y to CLYDE

(THERASE (ISA FRED ELEPHANT))
;; Remove the fact about Fred

(THGOAL (ISA FRED ELEPHANT))
;; Will fail since Fred is no longer asserted as an elephant
