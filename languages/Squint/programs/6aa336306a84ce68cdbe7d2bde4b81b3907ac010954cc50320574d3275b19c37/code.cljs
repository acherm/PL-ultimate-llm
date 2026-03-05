(defn fibonacci [n]
  (loop [a 0 b 1 count n]
    (if (= count 0)
      a
      (recur b (+ a b) (dec count)))))

(doseq [i (range 1 11)]
  (println (str "fib(" i ") = " (fibonacci i))))
