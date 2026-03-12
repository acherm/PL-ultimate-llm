;;; Meroon v3 - Geometric shapes example
;;; Demonstrates Meroon's class hierarchy, generic functions, and method dispatch

(define-class Shape Object ())

(define-class Circle Shape
  (radius))

(define-class Rectangle Shape
  (width height))

(define-generic (area self))

(define-method (area (self Circle))
  (* 3.14159265 (Circle-radius self) (Circle-radius self)))

(define-method (area (self Rectangle))
  (* (Rectangle-width self) (Rectangle-height self)))

(define-generic (perimeter self))

(define-method (perimeter (self Circle))
  (* 2 3.14159265 (Circle-radius self)))

(define-method (perimeter (self Rectangle))
  (* 2 (+ (Rectangle-width self) (Rectangle-height self))))

(define-generic (describe self))

(define-method (describe (self Circle))
  (display "Circle(r=")
  (display (Circle-radius self))
  (display "): area=")
  (display (area self))
  (display ", perimeter=")
  (display (perimeter self))
  (newline))

(define-method (describe (self Rectangle))
  (display "Rectangle(")
  (display (Rectangle-width self))
  (display "x")
  (display (Rectangle-height self))
  (display "): area=")
  (display (area self))
  (display ", perimeter=")
  (display (perimeter self))
  (newline))

(define shapes
  (list (make Circle 5)
        (make Rectangle 4 6)
        (make Circle 3)
        (make Rectangle 10 2)))

(for-each describe shapes)
