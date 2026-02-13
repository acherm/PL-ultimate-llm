(coalton-toplevel
  (declare quicksort (List Integer -> List Integer))
  (define (quicksort lst)
    (match lst
      ((Cons pivot rest)
       (let ((left (filter (fn (x) (<= x pivot)) rest))
             (right (filter (fn (x) (> x pivot)) rest)))
         (append (append (quicksort left) (make-list pivot))
                 (quicksort right))))
      ((Nil) Nil))))
