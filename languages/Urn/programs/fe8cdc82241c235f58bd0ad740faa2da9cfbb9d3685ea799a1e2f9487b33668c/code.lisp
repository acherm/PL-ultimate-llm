(defun factorial (n)
  (if (<= n 1)
    1
    (* n (factorial (- n 1)))))

(defun fizzbuzz (n)
  (cond
    [(= 0 (mod n 15)) "FizzBuzz"]
    [(= 0 (mod n 3))  "Fizz"]
    [(= 0 (mod n 5))  "Buzz"]
    [else              (number->string n)]))

(defun run-fizzbuzz (current limit)
  (when (<= current limit)
    (print! (fizzbuzz current))
    (run-fizzbuzz (+ current 1) limit)))

(run-fizzbuzz 1 30)