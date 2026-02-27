(defun quicksort (lst)
  (if (null lst)
      '()
      (let ((pivot (car lst))
            (rest (cdr lst)))
        (append
          (quicksort (remove-if-not #'(lambda (x) (< x pivot)) rest))
          (list pivot)
          (quicksort (remove-if-not #'(lambda (x) (>= x pivot)) rest))))))

(format t "Sorted: ~a~%" (quicksort '(3 1 4 1 5 9 2 6 5 3 5)))
