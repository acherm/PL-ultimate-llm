;;; FM synthesis instrument in CLM (Common Lisp Music)
;;; Demonstrates frequency modulation synthesis

(definstrument fm-violin (beg dur freq amp ratio index)
  "Simple FM synthesis instrument"
  (let* ((carrier (make-oscil freq))
         (modulator (make-oscil (* freq ratio)))
         (env (make-env (list 0 0 .1 1 .9 1 1 0)
                        :duration dur
                        :scaler amp))
         (ienv (make-env (list 0 0 .1 index .9 index 1 0)
                         :duration dur))
         (beg-samp (floor (* beg *srate*)))
         (end-samp (+ beg-samp (floor (* dur *srate*)))))
    (run
      (loop for i from beg-samp to end-samp do
        (outa i (* (env env)
                   (oscil carrier (* (env ienv)
                                     (oscil modulator)))))))))

(with-sound (:output "fm-test.aif" :srate 44100)
  (fm-violin 0 2.0 440 0.5 2.0 3.0)
  (fm-violin 2 2.0 660 0.5 2.0 2.5)
  (fm-violin 4 2.0 880 0.3 3.0 4.0))
