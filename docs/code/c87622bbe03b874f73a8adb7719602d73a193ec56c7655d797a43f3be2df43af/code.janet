(def width 40)
(def height 20)

(defn make-world []
  (array/new-filled (* width height) false))

(defn wrap [n max]
  (if (neg? n)
    (+ max n)
    (if (>= n max)
      (- n max)
      n)))

(defn idx [row col]
  (+ (* (wrap row height) width)
     (wrap col width)))

(defn neighbors [world row col]
  (def deltas [[-1 -1] [-1 0] [-1 1]
               [0 -1]         [0 1]
               [1 -1]  [1 0]  [1 1]])
  (sum (map (fn [[dr dc]]
              (if (get world (idx (+ row dr) (+ col dc))) 1 0))
            deltas)))

(defn step [world]
  (def new-world (make-world))
  (loop [row :range [0 height]
         col :range [0 width]
         :let [i (idx row col)
               n (neighbors world row col)]]
    (put new-world i
         (if (get world i)
           (<= 2 n 3)
           (= n 3))))
  new-world)

(defn show [world]
  (print "\e[H\e[2J")
  (loop [row :range [0 height]]
    (loop [col :range [0 width]]
      (prin (if (get world (idx row col)) "O" " ")))
    (print)))

(def init-world
  (let [w (make-world)]
    (put w (idx 1 1) true)
    (put w (idx 1 2) true)
    (put w (idx 1 3) true)
    w))

(var world init-world)
(forever
  (show world)
  (set world (step world))
  (ev/sleep 0.1))