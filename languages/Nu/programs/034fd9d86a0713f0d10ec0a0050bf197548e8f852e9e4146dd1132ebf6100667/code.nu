;; Factorial function in Nu
(function factorial (n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))

;; Test the function
(set result (factorial 5))
(puts "Factorial of 5 is: #{result}")
