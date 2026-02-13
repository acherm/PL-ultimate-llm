(defun quicksort (list)
  "Sort a list using the quicksort algorithm."
  (if (null list)
      nil
      (let ((pivot (car list))
            (rest (cdr list)))
        (append (quicksort (remove-if-not (lambda (x) (< x pivot)) rest))
                (list pivot)
                (quicksort (remove-if (lambda (x) (< x pivot)) rest))))))

;; Test the quicksort function
(print (quicksort '(3 7 8 5 2 1 9 5 4)))
