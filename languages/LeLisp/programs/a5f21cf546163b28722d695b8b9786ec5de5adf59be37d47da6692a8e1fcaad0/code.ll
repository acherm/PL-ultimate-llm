(de factorial (n)
  (if (= n 0)
    1
    (* n (factorial (- n 1)))))

(de main ()
  (let ((i 0))
    (while (<= i 10)
      (print (factorial i))
      (terpri)
      (setq i (+ i 1)))))

(main)
