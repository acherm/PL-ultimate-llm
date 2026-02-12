;;; Parallel sum in *Lisp
;;; Sum elements across all processors

(defun parallel-sum (data)
  (*set *data data)
  (*let ((local-sum (*sum *data)))
    (global-sum local-sum)))

(defun global-sum (value)
  (if (= (self) 0)
      value
      (send 0 value)))
