(define appendo
  (lambda (l s out)
    (conde
      ((== '() l) (== s out))
      ((fresh (a d res)
         (== `(,a . ,d) l)
         (== `(,a . ,res) out)
         (appendo d s res))))))

;; Example usage
(run* (q)
  (appendo '(1 2 3) '(4 5) q))
;; => ((1 2 3 4 5))