; Atomese knowledge representation example
; Demonstrates nodes, links, truth values, and pattern matching
; Running in OpenCog AtomSpace (Guile Scheme interface)

; Define entities with strength and confidence truth values (stv)
(ConceptNode "Fido" (stv 1.0 1.0))
(ConceptNode "Rex"  (stv 1.0 1.0))
(ConceptNode "dog"  (stv 1.0 1.0))
(ConceptNode "mammal" (stv 1.0 1.0))
(ConceptNode "animal" (stv 1.0 1.0))

; Inheritance relationships
(InheritanceLink (stv 1.0 1.0)
    (ConceptNode "Fido")
    (ConceptNode "dog"))

(InheritanceLink (stv 1.0 1.0)
    (ConceptNode "Rex")
    (ConceptNode "dog"))

(InheritanceLink (stv 1.0 1.0)
    (ConceptNode "dog")
    (ConceptNode "mammal"))

(InheritanceLink (stv 1.0 1.0)
    (ConceptNode "mammal")
    (ConceptNode "animal"))

; A relational predicate: Fido likes Rex
(PredicateNode "likes" (stv 1.0 1.0))

(EvaluationLink (stv 1.0 1.0)
    (PredicateNode "likes")
    (ListLink
        (ConceptNode "Fido")
        (ConceptNode "Rex")))

; Pattern match: find all X that inherit from "dog"
(define find-dogs
    (BindLink
        (VariableNode "$X")
        (InheritanceLink
            (VariableNode "$X")
            (ConceptNode "dog"))
        (VariableNode "$X")))

; Execute the query - returns a SetLink containing Fido and Rex
(cog-bind find-dogs)
