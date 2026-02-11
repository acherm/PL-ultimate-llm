(defquery gaussian-model
  "A simple Gaussian model"
  (let [mu (sample (normal 0 10))
        sigma (sample (gamma 1 1))]
    (observe (normal mu sigma) 5.0)
    (predict :mu mu)
    (predict :sigma sigma)))

(def samples
  (take 1000
        (doquery :lmh gaussian-model [])))

(def mu-samples (map :mu (map :result samples)))
(def sigma-samples (map :sigma (map :result samples)))

(println "Mean of mu:" (mean mu-samples))
(println "Mean of sigma:" (mean sigma-samples))
