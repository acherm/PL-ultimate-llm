(defn factorial [n]
  (if (<= n 1)
    1
    (* n (factorial (- n 1)))))

(console.log (factorial 5))
