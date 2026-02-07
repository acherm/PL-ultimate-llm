#!/usr/bin/env gxi
;; Fibonacci sequence generator using tail recursion

(def (fib n)
  (def (fib-iter a b count)
    (if (= count 0)
      a
      (fib-iter b (+ a b) (- count 1))))
  (fib-iter 0 1 n))

(def (main . args)
  (for (i (in-range 20))
    (displayln (fib i))))