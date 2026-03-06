(ns hello-arcadia.core
  (:use arcadia.core))

(defcomponent Greeter [self]
  (start [self]
    (log "Hello from Arcadia!")))

(hook+ (object-named "Main Camera") :start #'->Greeter)
