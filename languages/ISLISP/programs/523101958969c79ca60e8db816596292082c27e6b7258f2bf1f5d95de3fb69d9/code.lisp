;;;
;;; animal.lsp
;;;
;;;   Animal Guessing Game
;;;
;;;
;;; Copyright (C) 2006-2022 by T.Shido
;;;

(defclass <pair> ()
    ((key   :accessor pair-key   :initform nil)
     (value :accessor pair-value :initform nil)))

(defun make-pair (key value)
    (let ((p (create (class <pair>))))
        (setf (pair-key p) key)
        (setf (pair-value p) value)
        p))

(defun yes-or-no ()
    (let ((c (read-char)))
        (while (and (not (char= c #\y))
                    (not (char= c #\n)))
            (setq c (read-char)))
        (char= c #\y)))

(defun ask (question)
    (format (standard-output) "~A? (y/n) " question)
    (finish-output (standard-output))
    (yes-or-no))

(defun animal ()
    (let ((root (make-pair "Is it a mammal"
                           (make-pair "Does it have stripes"
                                      (make-pair "a tiger" nil)
                                      (make-pair "a lion" nil))
                           (make-pair "Is it a bird"
                                      (make-pair "a penguin" nil)
                                      (make-pair "a snake" nil)))))
        (while t
            (format (standard-output) "Think of an animal.~%")
            (let ((node root))
                (while (pair-value node)
                    (if (ask (pair-key node))
                        (setq node (pair-key (pair-value node)))
                        (setq node (pair-value (pair-value node)))))
                (if (ask (format-to-string "Is it ~A" (pair-key node)))
                    (format (standard-output) "I knew it!~%")
                    (progn
                        (format (standard-output) "What is it? ")
                        (let ((new-animal (read-line)))
                            (format (standard-output) "What is a question to distinguish ~A from ~A? "
                                new-animal (pair-key node))
                            (let ((new-question (read-line)))
                                (format (standard-output) "For ~A, what is the answer to the question? (y/n) "
                                    new-animal)
                                (if (yes-or-no)
                                    (setf (pair-value node)
                                          (make-pair (make-pair new-animal nil)
                                                     (make-pair (pair-key node) nil)))
                                    (setf (pair-value node)
                                          (make-pair (make-pair (pair-key node) nil)
                                                     (make-pair new-animal nil))))
                                (setf (pair-key node) new-question)))))))))