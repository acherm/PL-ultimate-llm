(defun c:drawcircle (/ pt rad)
  (setq pt (getpoint "\nSpecify center point: "))
  (if pt
    (progn
      (setq rad (getdist pt "\nSpecify radius: "))
      (if rad
        (command "._circle" pt rad)
        (princ "\nRadius not specified.")
      )
    )
    (princ "\nCenter point not specified.")
  )
  (princ)
)
