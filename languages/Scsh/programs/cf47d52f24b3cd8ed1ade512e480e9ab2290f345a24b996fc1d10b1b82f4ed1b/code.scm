#!/usr/bin/env scsh -s
!#
;;; File listing and filtering script in Scsh
;;; Demonstrates process notation and Scheme integration

(define (file-info file)
  (format #t "~a: ~a bytes~%"
          file
          (file-info:size (file-info file #t))))

(define (list-files-with-size dir)
  (let ((files (directory-files dir)))
    (for-each
     (lambda (file)
       (let ((path (string-append dir "/" file)))
         (if (file-readable? path)
             (file-info path))))
     files)))

;; Process notation: run external commands
(define (count-lines file)
  (run (wc -l ,file)))

;; Example: list current directory
(display "Files in current directory:")
(newline)
(list-files-with-size ".")
