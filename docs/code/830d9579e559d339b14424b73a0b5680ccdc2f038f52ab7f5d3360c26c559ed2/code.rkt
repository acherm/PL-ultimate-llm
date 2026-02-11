#lang racket
(require 2htdp/image 2htdp/universe)
(define SEGMENT-SIZE 20)
(define WIDTH  400)
(define HEIGHT 400)
(define BACKGROUND (empty-scene WIDTH HEIGHT))
(define HEAD (circle (/ SEGMENT-SIZE 2) "solid" "red"))
(define SEGMENT (circle (/ SEGMENT-SIZE 2) "solid" "blue"))
(define FOOD (circle (/ SEGMENT-SIZE 2) "solid" "green"))
(struct world (snake direction food))
(define (make-segment x y) (make-posn x y))
(define (random-food)
  (make-segment (* SEGMENT-SIZE (random (/ WIDTH SEGMENT-SIZE)))
                (* SEGMENT-SIZE (random (/ HEIGHT SEGMENT-SIZE)))))
(define (move-snake w)
  (match-define (world snake dir food) w)
  (define new-head
    (match dir
      ['up    (make-segment (posn-x (first snake)) (- (posn-y (first snake)) SEGMENT-SIZE))]
      ['down  (make-segment (posn-x (first snake)) (+ (posn-y (first snake)) SEGMENT-SIZE))]
      ['left  (make-segment (- (posn-x (first snake)) SEGMENT-SIZE) (posn-y (first snake)))]
      ['right (make-segment (+ (posn-x (first snake)) SEGMENT-SIZE) (posn-y (first snake)))]))
  (world (cons new-head (if (equal? new-head food)
                           snake
                           (drop-right snake 1)))
         dir
         (if (equal? new-head food)
             (random-food)
             food)))
(define (draw w)
  (match-define (world snake dir food) w)
  (define (place-segment img seg)
    (place-image SEGMENT (posn-x seg) (posn-y seg) img))
  (define with-segments
    (foldl place-segment BACKGROUND (rest snake)))
  (define with-head
    (place-image HEAD (posn-x (first snake)) (posn-y (first snake)) with-segments))
  (place-image FOOD (posn-x food) (posn-y food) with-head))
(define (change-dir w key)
  (match-define (world snake dir food) w)
  (world snake
         (match key
           ["up"    'up]
           ["down"  'down]
           ["left"  'left]
           ["right" 'right]
           [else dir])
         food))
(define initial-world
  (world (list (make-segment 200 200))
         'right
         (make-segment 100 100)))
(big-bang initial-world
  (to-draw draw)
  (on-tick move-snake 1/8)
  (on-key change-dir))