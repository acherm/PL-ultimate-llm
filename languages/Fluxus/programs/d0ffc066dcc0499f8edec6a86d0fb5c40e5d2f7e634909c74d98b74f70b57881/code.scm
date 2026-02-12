; Rotating cube in Fluxus
(define (animate)
    (rotate (vector (* (time) 50) (* (time) 30) 0))
    (draw-cube))

(every-frame (animate))
