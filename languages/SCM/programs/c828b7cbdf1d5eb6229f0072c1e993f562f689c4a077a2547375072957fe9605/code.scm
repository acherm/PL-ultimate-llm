;;; Towers of Hanoi in SCM (Scheme)
(define (hanoi n from to via)
  (if (= n 0)
      '()
      (begin
        (hanoi (- n 1) from via to)
        (display (string-append "Move disk " (number->string n)
                                " from " (symbol->string from)
                                " to " (symbol->string to)))
        (newline)
        (hanoi (- n 1) via to from))))

(hanoi 4 'A 'C 'B)
