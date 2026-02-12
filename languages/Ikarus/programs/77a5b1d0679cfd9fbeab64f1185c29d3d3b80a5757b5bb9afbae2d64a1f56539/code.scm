;;; Quicksort implementation in Ikarus Scheme
;;; This demonstrates list manipulation and recursion

(import (rnrs))

;; Partition a list into elements less than and greater than pivot
(define (partition pivot lst)
  (let loop ((lst lst) (less '()) (greater '()))
    (if (null? lst)
        (values (reverse less) (reverse greater))
        (let ((x (car lst)))
          (if (< x pivot)
              (loop (cdr lst) (cons x less) greater)
              (loop (cdr lst) less (cons x greater)))))))

;; Quicksort algorithm
(define (quicksort lst)
  (if (or (null? lst) (null? (cdr lst)))
      lst
      (let ((pivot (car lst))
            (rest (cdr lst)))
        (let-values (((less greater) (partition pivot rest)))
          (append (quicksort less)
                  (list pivot)
                  (quicksort greater))))))

;; Test the quicksort function
(define test-list '(64 34 25 12 22 11 90 88 45 50 23 36 18 77))

(display "Original list: ")
(display test-list)
(newline)

(display "Sorted list: ")
(display (quicksort test-list))
(newline)
