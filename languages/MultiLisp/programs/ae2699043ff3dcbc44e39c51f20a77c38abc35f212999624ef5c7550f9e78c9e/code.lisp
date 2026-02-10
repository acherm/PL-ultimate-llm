;;; Parallel Fibonacci in MultiLisp
;;; Demonstrates the 'future' construct for implicit parallelism

(define (pfib n)
  (if (< n 2)
      n
      (let ((a (future (pfib (- n 1))))
            (b (future (pfib (- n 2)))))
        (+ a b))))

(define (sequential-fib n)
  (if (< n 2)
      n
      (+ (sequential-fib (- n 1))
         (sequential-fib (- n 2)))))

;;; Parallel map using futures
(define (pmap f lst)
  (if (null? lst)
      '()
      (let ((head (future (f (car lst))))
            (tail (future (pmap f (cdr lst)))))
        (cons head tail))))

;;; Example: compute squares in parallel
(define (square x) (* x x))

(define (main)
  (display "Parallel Fibonacci:")
  (newline)
  (do ((i 0 (+ i 1)))
      ((= i 10))
    (display (pfib i))
    (display " "))
  (newline)
  (display "Parallel map (squares of 1-5): ")
  (display (pmap square '(1 2 3 4 5)))
  (newline))

(main)
