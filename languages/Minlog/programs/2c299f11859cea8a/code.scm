;; Minlog example: Addition is commutative for natural numbers
;; This proves that n + m = m + n

(load "~/minlog/init.scm")

(add-var-name "n" "m" (py "nat"))

;; Define addition commutativity
(set-goal "all n,m(n+m=m+n)")
(assume "n")
(ind)
;; Base case
(ng)
(use "Truth")
;; Inductive step
(assume "m" "IH")
(ng)
(use "IH")
(use "Truth")
