(be parent (tom bob))
(be parent (tom liz))
(be parent (bob ann))
(be parent (bob pat))

(be grandparent (@X @Z)
   (parent @X @Y)
   (parent @Y @Z) )

(be ancestor (@X @Y)
   (parent @X @Y) )

(be ancestor (@X @Y)
   (parent @X @Z)
   (ancestor @Z @Y) )

(pilog '((grandparent @GP @GC))
   (println @GP 'is 'grandparent 'of @GC) )

(pilog '((ancestor tom @D))
   (println @D 'is 'descendant 'of 'tom) )
