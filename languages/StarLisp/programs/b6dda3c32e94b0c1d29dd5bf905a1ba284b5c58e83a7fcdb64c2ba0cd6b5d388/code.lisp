;;; StarLisp: Parallel Vector Dot Product
;;; Demonstrates basic parallel operations on the Connection Machine
;;; Based on the StarLisp Reference Manual, Thinking Machines Corp., 1988

;; Declare parallel variables (pvars) -- one slot per processor
(*defvar *a* 0)
(*defvar *b* 0)
(*defvar *product* 0)

(defun init-vectors (n)
  "Initialize vectors: a[i] = i+1, b[i] = n-i for processors 0..n-1"
  (*when (<!! (self-address!!) (!! n))
    (*setf *a* (+!! (self-address!!) (!! 1)))
    (*setf *b* (-!! (!! n) (self-address!!)))))

(defun dot-product (n)
  "Compute dot product of two vectors of length n using parallel reduction"
  (init-vectors n)
  (*setf *product* (*!! *a* *b*))
  (*sum *product*))

;;; Compute dot product of [1,2,3,4,5] . [5,4,3,2,1]
;;; Expected: 1*5 + 2*4 + 3*3 + 4*2 + 5*1 = 5+8+9+8+5 = 35
(format t "Dot product result: ~a~%" (dot-product 5))
