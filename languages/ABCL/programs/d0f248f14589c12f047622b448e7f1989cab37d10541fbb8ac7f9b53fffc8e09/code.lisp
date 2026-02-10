; Counter actor example in ABCL/1
(defactor counter (count)
  (state ((val count))
    (=> (increment)
      (setq val (+ val 1))
      val)
    (=> (get)
      val)
    (=> (reset n)
      (setq val n)
      val)))

; Create and use a counter
(setq c (make-instance 'counter :count 0))
(c <= (increment))
(c <= (increment))
(c <= (get))
