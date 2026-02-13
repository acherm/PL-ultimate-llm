#lang frtime

;; Simple counter with reactive behavior
(define seconds (build-stream 0 add1))

(define counter
  (integral (constantly 1)))

(define doubled
  (* counter 2))

(printf "Counter: ~a~n" counter)
(printf "Doubled: ~a~n" doubled)
