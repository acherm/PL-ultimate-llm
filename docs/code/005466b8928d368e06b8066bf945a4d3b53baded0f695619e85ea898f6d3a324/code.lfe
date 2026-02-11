(defun fib (0)
  0)

(defun fib (1)
  1)

(defun fib (n)
  (+ (fib (- n 1)) (fib (- n 2))))

;; Example usage:
;; (fib 10)