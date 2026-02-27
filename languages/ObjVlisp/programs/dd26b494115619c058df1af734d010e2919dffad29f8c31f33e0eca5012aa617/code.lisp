;;; ObjVLisp: Point class example
;;; The ObjVLisp kernel defines two primitive classes:
;;; - Objet: the root of the inheritance hierarchy
;;; - Classe: the metaclass (its own instance)
;;; See: Cointe, P. (1987) "ObjVLisp: A Uniform, Reflective Object-Oriented
;;; Language Based on a Kernel of First Class Types." OOPSLA'87.

;;; Create the Point class
(define Point
  (send Classe 'new
        :name   'Point
        :supers (list Objet)
        :iv     '(x y)))

;;; Add a method to compute distance from origin
(send Point 'defmethod 'magnitude
  (lambda (self)
    (sqrt (+ (* (send self 'x) (send self 'x))
             (* (send self 'y) (send self 'y))))))

;;; Add a method to display the point
(send Point 'defmethod 'show
  (lambda (self)
    (display "Point(")
    (display (send self 'x))
    (display ", ")
    (display (send self 'y))
    (display ")")))

;;; Instantiate Point objects
(define p1 (send Point 'new :x 3 :y 4))
(define p2 (send Point 'new :x 0 :y 0))

;;; Send messages to the instances
(send p1 'show)                   ;;; => Point(3, 4)
(newline)
(display (send p1 'magnitude))    ;;; => 5
(newline)
(send p2 'show)                   ;;; => Point(0, 0)
(newline)
(display (send p2 'magnitude))    ;;; => 0
(newline)
