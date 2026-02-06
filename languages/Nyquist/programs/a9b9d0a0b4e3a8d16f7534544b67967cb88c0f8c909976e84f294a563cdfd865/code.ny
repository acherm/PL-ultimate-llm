;; Simple sine wave tone generator
;; Generates a 440 Hz tone (A4) for 1 second

(play
  (osc (hz-to-step 440) 1.0))
