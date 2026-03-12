;; Sieve of Eratosthenes in Gambit Scheme
;; Finds all prime numbers up to a given limit

(define (sieve limit)
  (let ((composite (make-vector (+ limit 1) #f)))
    (let loop ((i 2) (primes '()))
      (cond
        ((> i limit)
         (reverse primes))
        ((vector-ref composite i)
         (loop (+ i 1) primes))
        (else
         (let mark ((j (* i i)))
           (when (<= j limit)
             (vector-set! composite j #t)
             (mark (+ j i))))
         (loop (+ i 1) (cons i primes)))))))

(define primes-to-50 (sieve 50))
(display "Primes up to 50: ")
(display primes-to-50)
(newline)

(display "Count: ")
(display (length primes-to-50))
(newline)
