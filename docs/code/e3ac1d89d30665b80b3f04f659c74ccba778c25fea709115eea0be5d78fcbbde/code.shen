(package pattern [intern]

(define unify
  X X _ -> true
  X Y Dict -> (unify-h X Y Dict))

(define unify-h
  X Y Dict -> (let Value+- (assoc X Dict)
                  (if (value? Value+-)
                      (= Y (value-> Value+-))
                      (let NewDict (do (dict-update X Y Dict)
                                      (dict-update Y X Dict))
                           true)))
                where (variable? X)
  X Y Dict -> (let Value+- (assoc Y Dict)
                  (if (value? Value+-)
                      (= X (value-> Value+-))
                      (let NewDict (do (dict-update X Y Dict)
                                      (dict-update Y X Dict))
                           true)))
                where (variable? Y)
  [X | Y] [W | Z] Dict -> (and (unify X W Dict) 
                               (unify Y Z Dict))
                          where (and (cons? [X | Y]) 
                                    (cons? [W | Z]))
  _ _ _ -> false)