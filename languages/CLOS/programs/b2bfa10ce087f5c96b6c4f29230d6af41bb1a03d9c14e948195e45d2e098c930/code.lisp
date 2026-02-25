(defclass shape ()
  ((color :reader shape-color
          :initarg :color
          :initform :white)))

(defclass circle (shape)
  ((radius :reader circle-radius
           :initarg :radius)))

(defgeneric area (shape)
  (:documentation "Compute the area of a shape."))

(defmethod area ((c circle))
  (* pi (expt (circle-radius c) 2)))

(let ((c (make-instance 'circle :radius 5 :color :blue)))
  (format t "Circle color: ~A~%" (shape-color c))
  (format t "Circle area: ~F~%" (area c)))
