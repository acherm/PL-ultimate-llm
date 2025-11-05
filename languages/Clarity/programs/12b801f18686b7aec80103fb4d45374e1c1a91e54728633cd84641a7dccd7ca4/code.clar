(define-data-var count uint u0)

(define-read-only (get-count)
  (var-get count))

(define-public (increment)
  (begin
    (var-set count (+ u1 (var-get count)))
    (ok true)))

(define-public (decrement)
  (begin
    (if (> (var-get count) u0)
      (begin
        (var-set count (- (var-get count) u1))
        (ok true))
      (err u0))))

(define-public (reset)
  (begin
    (var-set count u0)
    (ok true)))