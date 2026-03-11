;;; CommonLoops example: Shape area computation
;;; From: Bobrow et al., "CommonLoops: Merging Lisp and Object-Oriented
;;; Programming", OOPSLA 1986, ACM SIGPLAN Notices 21(11):17-29

(defclass shape ()
  ((color :initarg :color :accessor shape-color)))

(defclass circle (shape)
  ((radius :initarg :radius :accessor circle-radius)))

(defclass rectangle (shape)
  ((width  :initarg :width  :accessor rect-width)
   (height :initarg :height :accessor rect-height)))

(defmethod area ((c circle))
  (* pi (expt (circle-radius c) 2)))

(defmethod area ((r rectangle))
  (* (rect-width r) (rect-height r)))

(defmethod print-info ((s shape))
  (format t "~a shape, color ~a, area ~,2f~%"
          (class-name (class-of s))
          (shape-color s)
          (area s)))

(let ((c (make-instance 'circle
                        :color 'red
                        :radius 5))
      (r (make-instance 'rectangle
                        :color 'blue
                        :width 4
                        :height 6)))
  (print-info c)
  (print-info r))
