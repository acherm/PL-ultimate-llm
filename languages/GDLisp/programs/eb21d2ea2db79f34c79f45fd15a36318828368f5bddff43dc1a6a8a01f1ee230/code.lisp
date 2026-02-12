(defn factorial (n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

(defn main ()
  (print (factorial 5))
  (print (factorial 10)))
