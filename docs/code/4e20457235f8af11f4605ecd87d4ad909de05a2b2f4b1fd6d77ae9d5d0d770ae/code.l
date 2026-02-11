(de life (Size Grid Steps)
   (let Grid (if Grid @ (need (* Size Size) (fill '((T . NIL)))))
      (for I Steps
         (disp Grid Size)
         (wait 500)
         (setq Grid
            (make
               (for (Y . @) Size
                  (link
                     (for (X . @) Size
                        (link
                           (let Sum
                              (sum
                                 '((Y X)
                                    (+ (get Grid (mod (+ Y -1) Size) (mod (+ X -1) Size))
                                       (get Grid (mod (+ Y -1) Size) X)
                                       (get Grid (mod (+ Y -1) Size) (mod (+ X 1) Size))
                                       (get Grid Y (mod (+ X -1) Size))
                                       (get Grid Y (mod (+ X 1) Size))
                                       (get Grid (mod (+ Y 1) Size) (mod (+ X -1) Size))
                                       (get Grid (mod (+ Y 1) Size) X)
                                       (get Grid (mod (+ Y 1) Size) (mod (+ X 1) Size)) ) ) )
                              (or (and (= Sum 3) 1)
                                 (and (= Sum 2) (get Grid Y X)) ) ) ) ) ) ) ) ) ) )

(de disp (Grid Size)
   (for (Y . @) Size
      (for (X . @) Size
         (prin (if (get Grid Y X) "[]" " .") ) )
      (prinl) ) )