#lang pollen

◊(define (em . words)
   `(strong ((class "emphatically")) ,@words))

◊h1{Welcome to Pollen}

This is a ◊em{simple} example of Pollen markup.

◊(apply string-append (map (lambda (x) (format "Item ~a " x)) (range 1 4)))
