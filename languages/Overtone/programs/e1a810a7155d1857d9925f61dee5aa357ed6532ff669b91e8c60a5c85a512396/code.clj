(ns overtone-example
  (:use [overtone.live]))

;; Define a simple synthesizer instrument
(definst saw-wave [freq 440 attack 0.01 sustain 0.4 release 0.1 vol 0.4]
  (* (env-gen (env-lin attack sustain release) 1 1 0 1 FREE)
     (saw freq)
     vol))

;; Define a chord progression
(defn play-chord [notes]
  (doseq [note notes]
    (saw-wave (midi->hz note))))

;; Play a simple melody
(defn melody []
  (let [notes [60 62 64 65 67 69 71 72]]
    (doseq [note notes]
      (saw-wave (midi->hz note))
      (Thread/sleep 300))))