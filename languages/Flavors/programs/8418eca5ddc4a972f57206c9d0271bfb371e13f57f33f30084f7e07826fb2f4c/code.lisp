;;; Simple example of Flavors object-oriented programming
;;; Define a flavor for a point in 2D space

(defflavor point (x y)
  ()
  :gettable-instance-variables
  :initable-instance-variables)

(defmethod (point :distance-from-origin) ()
  (sqrt (+ (* x x) (* y y))))

(defmethod (point :move) (dx dy)
  (setq x (+ x dx))
  (setq y (+ y dy)))

;;; Create an instance
(setq my-point (make-instance 'point :x 3 :y 4))

;;; Get distance from origin
(send my-point :distance-from-origin)  ; Returns 5.0

;;; Move the point
(send my-point :move 1 1)
