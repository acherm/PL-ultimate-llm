; Towers of Hanoi in S9fES (Scheme 9 from Empty Space)
; Classic recursive solution demonstrating S9fES Scheme

(define (hanoi n from to via)
  (if (> n 0)
      (begin
        (hanoi (- n 1) from via to)
        (display (list 'move 'disk n 'from from 'to to))
        (newline)
        (hanoi (- n 1) via to from))))

(hanoi 3 'left 'right 'center)
