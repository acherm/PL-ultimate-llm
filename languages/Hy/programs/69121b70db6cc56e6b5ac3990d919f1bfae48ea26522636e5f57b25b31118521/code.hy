(import [time [sleep]]
        [random [randint]])

(defn create-board [width height]
  (list-comp
    (list-comp
      (if (= 1 (randint 0 1)) "*" " ")
      [x (range width)])
    [y (range height)]))

(defn count-neighbours [board x y width height]
  (setv count 0)
  (for [i (range -1 2)]
    (for [j (range -1 2)]
      (if (and
            (!= (+ i j) 0)
            (< -1 (+ x i) width)
            (< -1 (+ y j) height)
            (= (get-in board [(+ y j) (+ x i)]) "*"))
        (setv count (+ count 1)))))
  count)

(defn step [board width height]
  (setv new-board
    (list-comp
      (list-comp
        (get-in board [y x])
        [x (range width)])
      [y (range height)]))
  (for [y (range height)]
    (for [x (range width)]
      (setv n (count-neighbours board x y width height))
      (setv cell (get-in board [y x]))
      (cond [(and (= cell "*") (< n 2))
             (setv (get-in new-board [y x]) " ")]
            [(and (= cell "*") (> n 3))
             (setv (get-in new-board [y x]) " ")]
            [(and (= cell " ") (= n 3))
             (setv (get-in new-board [y x]) "*")])))
  new-board)

(defn print-board [board width height]
  (print "\033[2J\033[H")
  (for [y (range height)]
    (for [x (range width)]
      (print (get-in board [y x]) :end ""))
    (print)))

(defmain [&rest args]
  (setv width 30)
  (setv height 15)
  (setv board (create-board width height))
  (while True
    (print-board board width height)
    (setv board (step board width height))
    (sleep 0.1)))