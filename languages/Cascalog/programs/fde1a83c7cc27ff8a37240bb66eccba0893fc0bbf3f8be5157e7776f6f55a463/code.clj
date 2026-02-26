(defmapcatop split [sentence]
  (seq (.split sentence "\\s+")))

(?<- (stdout) [?word ?count] (sentence ?s)
  (split ?s :> ?word) (c/count ?count))
