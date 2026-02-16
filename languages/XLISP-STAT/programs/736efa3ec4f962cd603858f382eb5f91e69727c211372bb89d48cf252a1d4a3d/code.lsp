; XLISP-STAT program to compute descriptive statistics
; Define a list of data points
(def data (list 12 15 18 21 24 27 30))

; Compute the mean
(defun compute-mean (values)
  (/ (apply #'+ values) (length values)))

; Compute the standard deviation
(defun compute-stddev (values)
  (let* ((n (length values))
         (m (compute-mean values))
         (squared-diffs (mapcar #'(lambda (x) (expt (- x m) 2)) values))
         (variance (/ (apply #'+ squared-diffs) n)))
    (sqrt variance)))

; Display results
(format t "Data: ~a~%" data)
(format t "Mean: ~a~%" (compute-mean data))
(format t "Standard Deviation: ~a~%" (compute-stddev data))
