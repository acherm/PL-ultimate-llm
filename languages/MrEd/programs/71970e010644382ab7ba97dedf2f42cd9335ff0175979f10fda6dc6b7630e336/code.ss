#lang mzscheme

(require (lib "mred.ss" "mred")
         (lib "class.ss"))

; A simple counter application using the MrEd GUI toolkit
(define frame
  (make-object frame% "MrEd Counter" #f 300 150))

(define panel
  (make-object vertical-panel% frame))

(define count 0)

(define label
  (make-object message% "Count: 0" panel))

(define button
  (make-object button% "Increment" panel
    (lambda (b e)
      (set! count (+ count 1))
      (send label set-label (format "Count: ~a" count)))))

(send frame show #t)
