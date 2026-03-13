;; Fibonacci sequence using Clojure CLR
(defn fib [n]
  (loop [a 0 b 1 cnt n]
    (if (zero? cnt)
      a
      (recur b (+ a b) (dec cnt)))))

(doseq [i (range 10)]
  (println (str "fib(" i ") = " (fib i))))
