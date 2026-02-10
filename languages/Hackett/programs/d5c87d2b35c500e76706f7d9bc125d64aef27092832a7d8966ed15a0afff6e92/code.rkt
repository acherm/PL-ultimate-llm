#lang hackett

(defn factorial : {Integer -> Integer}
  [[0] 1]
  [[n] (* n (factorial (- n 1)))])

(defn main : (IO Unit)
  (do (println! (show (factorial 5)))
      (println! (show (factorial 10)))))
